from flask import Blueprint, render_template, request
from celery.result import AsyncResult

from .tasks import mytask

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/task/start", methods=["POST"])
def task_start():
    task = mytask.delay(10)
    return {"task_id": task.id}

@main.route("/task/progress", methods=["POST"])
def task_progress():
    data = request.get_json()
    task = AsyncResult(data["task_id"])
    return {"state": task.state, "progress": task.info.get("progress", 0)}