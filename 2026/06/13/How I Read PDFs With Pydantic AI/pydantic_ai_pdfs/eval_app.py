"""Flask app for manually evaluating AI runs traced to Phoenix.

Reads runs (LLM spans that were sent a PDF) from the Phoenix SQLite database
and records human feedback via the Phoenix annotation API, so evaluations
also appear in the Phoenix UI.

Run with:  uv run python eval_app.py
"""

import base64
import json
import os
import sqlite3
from pathlib import Path

import httpx
from flask import Flask, Response, abort, flash, redirect, render_template, request, url_for

PHOENIX_DB = Path(os.environ.get("PHOENIX_DB", Path.home() / ".phoenix" / "phoenix.db"))
PHOENIX_URL = os.environ.get("PHOENIX_URL", "http://localhost:6006")
ANNOTATION_NAME = "correctness"

app = Flask(__name__)
app.secret_key = "local-eval-app"


def db():
    conn = sqlite3.connect(f"file:{PHOENIX_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def parse_json(value, default=None):
    if isinstance(value, (list, dict)):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return default


def extract_pdf_part(attrs):
    """Return the first application/pdf blob part from the input messages."""
    messages = parse_json(attrs.get("gen_ai", {}).get("input", {}).get("messages"), [])
    for message in messages:
        for part in message.get("parts", []):
            if part.get("type") == "blob" and "pdf" in str(part.get("mime_type", "")):
                return part
    return None


def extract_prompt(attrs):
    """System instructions plus any user text parts, as a list of (role, text)."""
    prompt = []
    for item in parse_json(attrs.get("gen_ai", {}).get("system_instructions"), []):
        if item.get("content"):
            prompt.append(("system", item["content"]))
    messages = parse_json(attrs.get("gen_ai", {}).get("input", {}).get("messages"), [])
    for message in messages:
        for part in message.get("parts", []):
            if part.get("type") == "text" and part.get("content"):
                prompt.append((message.get("role", "user"), part["content"]))
    return prompt


def build_run(row, attrs=None):
    attrs = attrs if attrs is not None else json.loads(row["attributes"])
    pdf_part = extract_pdf_part(attrs)
    output_raw = attrs.get("output", {}).get("value")
    output = parse_json(output_raw)
    if isinstance(output, str):  # output.value is double-JSON-encoded
        output = parse_json(output)

    # Reconciliation check mirroring script.py: beginning + transactions == current
    reconciliation = None
    if isinstance(output, dict) and isinstance(output.get("transactions"), list):
        try:
            total = round(sum(t["amount"] for t in output["transactions"]), 2)
            expected = round(output["beginning_balance"] + total, 2)
            reconciliation = {
                "transactions_total": total,
                "expected_balance": expected,
                "matches": expected == round(output["current_balance"], 2),
            }
        except (KeyError, TypeError):
            pass

    return {
        "span_id": row["span_id"],
        "trace_id": row["trace_id"],
        "start_time": row["start_time"],
        "status_code": row["status_code"],
        "status_message": row["status_message"],
        "model": attrs.get("llm", {}).get("model_name") or row["name"],
        "prompt": extract_prompt(attrs),
        "output": output,
        "output_raw": output_raw,
        "pdf_size_kb": len(pdf_part["content"]) * 3 // 4 // 1024 if pdf_part else None,
        "tokens_prompt": row["llm_token_count_prompt"],
        "tokens_completion": row["llm_token_count_completion"],
        "cost": attrs.get("operation", {}).get("cost"),
        "reconciliation": reconciliation,
        "feedback": {
            "label": row["fb_label"],
            "explanation": row["fb_explanation"],
            "updated_at": row["fb_updated_at"],
        }
        if row["fb_label"]
        else None,
    }


RUNS_QUERY = """
    SELECT s.span_id, s.name, s.start_time, s.status_code, s.status_message,
           s.attributes, s.llm_token_count_prompt, s.llm_token_count_completion,
           t.trace_id,
           sa.label AS fb_label, sa.explanation AS fb_explanation, sa.updated_at AS fb_updated_at
    FROM spans s
    JOIN traces t ON s.trace_rowid = t.id
    LEFT JOIN span_annotations sa ON sa.span_rowid = s.id AND sa.name = ?
    WHERE s.span_kind = 'LLM' AND s.attributes LIKE '%application/pdf%'
    ORDER BY s.start_time DESC
"""


def load_runs():
    with db() as conn:
        rows = conn.execute(RUNS_QUERY, (ANNOTATION_NAME,)).fetchall()
    runs = []
    for row in rows:
        attrs = json.loads(row["attributes"])
        if extract_pdf_part(attrs):
            runs.append(build_run(row, attrs))
    return runs


@app.route("/")
def index():
    runs = load_runs()
    filter_by = request.args.get("filter", "all")
    counts = {
        "all": len(runs),
        "unreviewed": sum(1 for r in runs if not r["feedback"]),
        "correct": sum(1 for r in runs if r["feedback"] and r["feedback"]["label"] == "correct"),
        "incorrect": sum(1 for r in runs if r["feedback"] and r["feedback"]["label"] == "incorrect"),
    }
    if filter_by == "unreviewed":
        runs = [r for r in runs if not r["feedback"]]
    elif filter_by in ("correct", "incorrect"):
        runs = [r for r in runs if r["feedback"] and r["feedback"]["label"] == filter_by]
    return render_template("index.html", runs=runs, filter_by=filter_by, counts=counts)


def get_run_or_404(span_id):
    runs = load_runs()
    for i, run in enumerate(runs):
        if run["span_id"] == span_id:
            prev_run = runs[i - 1]["span_id"] if i > 0 else None
            next_run = runs[i + 1]["span_id"] if i + 1 < len(runs) else None
            return run, prev_run, next_run
    abort(404)


@app.route("/run/<span_id>")
def run_detail(span_id):
    run, prev_run, next_run = get_run_or_404(span_id)
    return render_template("run.html", run=run, prev_run=prev_run, next_run=next_run)


@app.route("/run/<span_id>/pdf")
def run_pdf(span_id):
    with db() as conn:
        row = conn.execute("SELECT attributes FROM spans WHERE span_id = ?", (span_id,)).fetchone()
    if row is None:
        abort(404)
    part = extract_pdf_part(json.loads(row["attributes"]))
    if part is None:
        abort(404)
    return Response(
        base64.b64decode(part["content"]),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"inline; filename={span_id}.pdf"},
    )


@app.route("/run/<span_id>/feedback", methods=["POST"])
def run_feedback(span_id):
    label = request.form.get("label")
    if label not in ("correct", "incorrect"):
        abort(400)
    notes = request.form.get("notes", "").strip()
    payload = {
        "data": [
            {
                "span_id": span_id,
                "name": ANNOTATION_NAME,
                "annotator_kind": "HUMAN",
                "result": {
                    "label": label,
                    "score": 1.0 if label == "correct" else 0.0,
                    "explanation": notes or None,
                },
                "metadata": {},
            }
        ]
    }
    try:
        response = httpx.post(
            f"{PHOENIX_URL}/v1/span_annotations",
            params={"sync": "true"},
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        flash(f"Feedback saved: {label}", "success")
    except httpx.HTTPError as exc:
        flash(f"Could not save feedback via Phoenix at {PHOENIX_URL}: {exc}", "error")

    if request.form.get("next") and request.form.get("next_run"):
        return redirect(url_for("run_detail", span_id=request.form["next_run"]))
    return redirect(url_for("run_detail", span_id=span_id))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
