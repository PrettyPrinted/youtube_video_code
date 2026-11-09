from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai_compatible import OpenAICompatibleProvider

model = OpenAIChatModel(
    'nvidia/nemotron-3-nano-4b',
    provider=OpenAICompatibleProvider(
        'lm-studio',
        base_url='http://127.0.0.1:1234/v1',
    ),
)
agent = Agent(model)

result = agent.run_sync("Hello!")

print(result.output)