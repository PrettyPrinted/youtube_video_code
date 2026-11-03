from dotenv import load_dotenv
from openai import OpenAI
from rich import print

load_dotenv()

client = OpenAI()
    
def generate_response(user_message):
    response = client.responses.create(
        model="gpt-6-astra",
        input=user_message,
    )

    return response


if __name__ == "__main__":
    print("[blue]Ask your agent to do anything.[/blue]")

    question = input()
    response = generate_response(question)

    print(f"[green]{response.output_text}[/green]")