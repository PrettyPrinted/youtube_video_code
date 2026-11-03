import os
import json
import subprocess

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from rich import print

load_dotenv("/home/anthony/myagent/.env")

client = OpenAI()

tools = [
    {
        "type": "function",
        "name": "list_files",
        "description": "List the files in the working directory"
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "Read the contents of the filename given",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"}
            },
            "required": ["filename"]
        }
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write text data to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to be written to a file."},
                "filename": {"type": "string", "description": "The name of the file."}
            },
            "required": ["text", "filename"],
        }
    },
    {
        "type": "function",
        "name": "execute_command",
        "description": "Execute a unix command on the user's system",
        "parameters": {
            "type": "object",
            "properties": {
                "arguments": {"type": "array"}
            },
            "required": ["arguments"]
        }
    }
]

def list_files():
    return str(os.listdir())

def write_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)

def read_file(filename):
    with open(filename, "r") as f:
        return f.read()

def execute_command(arguments):
    try:
        result = subprocess.run(arguments, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return repr(e)
    
def generate_response(inputdata, previous_response_id=None):
    response = client.responses.create(
        model="gpt-6-astra",
        input=inputdata,
        tools=tools,
        previous_response_id=previous_response_id,
    )
    while True:
        input_messages = []

        for item in response.output:
            if item.type == "function_call":
                print(f"[yellow]Calling {item.name} with {item.arguments}[/yellow]")
                if item.name == "list_files":
                    input_messages.append(
                        {
                            "type": "function_call_output", 
                            "call_id": item.call_id, 
                            "output": list_files()
                        }
                    )

                if item.name == "write_file":
                    text = json.loads(item.arguments)["text"]
                    filename = json.loads(item.arguments)["filename"]

                    write_file(filename, text)

                    input_messages.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": "Success"
                        }
                    )

                if item.name == "read_file":
                    filename = json.loads(item.arguments)["filename"]
                    input_messages.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": read_file(filename)
                        }
                    )

                if item.name == "execute_command":
                    arguments = json.loads(item.arguments)["arguments"]
                    print(f"[yellow]The agent wants to run {arguments}. Is that OK (y/n)?[/yellow]")
                    answer = input()
                    if answer == "y":
                        input_messages.append(
                            {
                                "type": "function_call_output",
                                "call_id": item.call_id,
                                "output": execute_command(arguments)
                            }
                        )
                    else:
                        input_messages.append(
                            {
                                "type": "function_call_output",
                                "call_id": item.call_id,
                                "output": "The user did not give you permission to execute that command."
                            }
                        )

        if not input_messages:
            return response
        
        response = client.responses.create(
            model="gpt-6-astra",
            input=input_messages,
            tools=tools,
            previous_response_id=response.id,
        )

def main():
    working_dir = Path.cwd()
    print(f"[blue]Working in: {working_dir}[/blue]")
    print("[blue]Ask your agent to do anything.[/blue]")

    previous_response_id = None

    while True:
        question = input()
        response = generate_response(question, previous_response_id)
        previous_response_id = response.id

        print(f"[green]{response.output_text}[/green]")

if __name__ == "__main__":
    main()