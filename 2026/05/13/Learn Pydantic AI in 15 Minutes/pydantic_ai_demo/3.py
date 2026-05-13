import logfire

from dataclasses import dataclass
from pydantic_ai import Agent

logfire.configure()
logfire.instrument_pydantic_ai()

transactions = [
    {"description": "MOBILE PURCHASE CHIPOTLE", "amount": 10.50},
    {"description": "AMAZON.COM", "amount": 125.71},
    {"description": "CHECKCARD DAVE'S", "amount": 39.11},
]

agent = Agent(instructions="You are a transaction categorizer.")

result = agent.run_sync(f"{transactions}", model="gpt-4")

print(result)