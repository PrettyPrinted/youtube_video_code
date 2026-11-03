from dotenv import load_dotenv
from openai import OpenAI
from rich import print

load_dotenv()

client = OpenAI()
    
def generate_response(user_message, previous_response_id=None):
    response = client.responses.create(
        model="gpt-6-astra",
        input=user_message,
        previous_response_id=previous_response_id,
    )

    return response


if __name__ == "__main__":
    print("[blue]Ask your agent to do anything.[/blue]")

    previous_response_id = None

    while True:
        question = input()
        response = generate_response(question, previous_response_id)
        previous_response_id = response.id

        print(f"[green]{response.output_text}[/green]")