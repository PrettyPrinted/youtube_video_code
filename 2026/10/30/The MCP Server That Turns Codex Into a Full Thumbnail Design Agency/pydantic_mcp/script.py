import os

from pydantic_ai import Agent
from pydantic_ai.capabilities import MCP
from fastmcp import Client
from fastmcp.client.auth import OAuth
from key_value.aio.stores.disk import DiskStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet


# key = Fernet.generate_key()
# print(key)

# Create encrypted disk storage
encrypted_storage = FernetEncryptionWrapper(
    key_value=DiskStore(directory="/Users/anthony/Desktop/pydantic_mcp/.fastmcp/oauth-tokens"),
    fernet=Fernet(b'fernet key')
)

oauth = OAuth(scopes=["user"], token_storage=encrypted_storage)
client = Client("https://mcp.higgsfield.ai/mcp", auth=oauth)

agent = Agent(
    'openai:gpt-6.1-sol',
    capabilities=[
        MCP(local=client)    
    ],
)

result = agent.run_sync("Generate a thumbnail for a beginner Flask video. do not ask any follow up questions")

print(result.output)
