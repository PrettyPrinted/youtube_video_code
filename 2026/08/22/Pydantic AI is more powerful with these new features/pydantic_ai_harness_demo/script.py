from pydantic_ai import Agent
from pydantic_ai_harness import Coder, Memory
from pydantic_ai_harness.memory import FileStore

agent = Agent('openai:gpt-5.6-sol', capabilities=[Memory(FileStore('.memories'))])

print("Running agent...")
result = agent.run_sync("What should I have for dinner tonight?")

print("Agent output:")
print(result.output)