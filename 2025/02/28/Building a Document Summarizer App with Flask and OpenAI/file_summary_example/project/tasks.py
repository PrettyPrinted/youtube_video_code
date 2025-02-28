from markitdown import MarkItDown
from openai import OpenAI

from .extensions import db
from .models import File

def process_file(app_context, filename, path):
    with app_context:
        md = MarkItDown()
        result = md.convert(path)

        client = OpenAI()

        messages = [
            {
                "role": "system",
                "content": "You are an assistant that summarizes text documents. Summarize the following text and give output as markdown using a few headers"
            },
            {
                "role": "user",
                "content": f"<text>{result.text_content[:20000]}</text>"
            }
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-4o"
        )

        summary = chat_completion.choices[0].message.content

        file = File(
            filename=filename,
            path=path,
            content=result.text_content,
            summary=summary
        )

        db.session.add(file)
        db.session.commit()