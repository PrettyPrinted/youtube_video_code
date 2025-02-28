from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown()
result = md.convert("Cooking.pdf")

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "You are an assistant that summarizes text documents. Summarize the following text"
    },
    {
        "role": "user",
        "content": f"<text>{result.text_content}</text>"
    }
]

chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-4o"
)

print(chat_completion.choices[0].message.content)