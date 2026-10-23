import os
import time
import requests

from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import Literal

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

r = requests.get(f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_API_KEY}&id=GnIREMgz-SQ&part=snippet")

start = time.perf_counter()


title = r.json()["items"][0]["snippet"]["title"]
description = r.json()["items"][0]["snippet"]["description"]
thumbnail_url = r.json()["items"][0]["snippet"]["thumbnails"]["maxres"]["url"]

print(description)

# agent = Agent('openai:gpt-6.1-sol', instructions="Tell me if this is an educational or entertainment video")

# result = agent.run_sync(f"TITLE: {title} DESCRIPTION: {description}")

class Analysis(BaseModel):
    is_educational: bool = Field(description="Is this video educational?")
    primary_product: Literal["course", "coaching", "physical product", "service", "software"] = Field(description="What is the primary product they're selling in the description")


agent = Agent('typesafe:jev-latest', output_type=Analysis)

result = agent.run_sync(f"TITLE: {title} DESCRIPTION: {description}")

print(result.output)
print(result.usage)
print(result.response.provider_details)


elapsed = time.perf_counter() - start
print(f"Took {elapsed:.2f} seconds")