import logfire

from dataclasses import dataclass
from pydantic_ai import Agent
from pydantic import BaseModel

logfire.configure()
logfire.instrument_pydantic_ai()

transactions = [
    {"description": "MOBILE PURCHASE CHIPOTLE", "amount": 10.50},
    {"description": "AMAZON.COM", "amount": 125.71},
    {"description": "CHECKCARD DAVE'S", "amount": 39.11},
]

class Transactions(BaseModel):
    description: str
    amount: float
    category: str

class Output(BaseModel):
    transactions: list[Transactions]

agent = Agent(output_type=Output, instructions="You are a transaction categorizer. Look up the merchant information only for the descriptions that aren't obvious. If you don't get a match, do your best to categorize it. Return the category for each transaction.")

MERCHANT_DB = {
    "MOBILE PURCHASE CHIPOTLE": {"name": "Chipotle", "business_type": "Restaurant"},
    "CHECKCARD DAVE'S": {"name": "Dave's", "business_type": "Convenience Store"},
}

@agent.tool_plain
def merchant_lookup(description: str):
    return MERCHANT_DB.get(description, {"name": "Unknown", "business_type": "Unknown"})

result = agent.run_sync(f"{transactions}", model="gpt-4")

print(result)