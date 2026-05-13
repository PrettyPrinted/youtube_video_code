import logfire

from dataclasses import dataclass
from pydantic_ai import Agent

logfire.configure()
logfire.instrument_pydantic_ai()

agent = Agent()

result = agent.run_sync("How many planets are in the solar system?", model="gpt-4")

print(result)
