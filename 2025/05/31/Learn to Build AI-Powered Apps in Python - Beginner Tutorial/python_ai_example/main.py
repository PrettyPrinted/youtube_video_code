import os

from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent, Tool

from helpers import SCREENSHOTS_DIRECTORY, rename_and_move_screenshot
from helpers import list_categories, get_newest_screenshot, create_directory

newest_screenshot = get_newest_screenshot()

with open(os.path.join(SCREENSHOTS_DIRECTORY, newest_screenshot), "rb") as file:
    data = file.read()

rename_file_agent = Agent(
    "openai:gpt-4.1-mini-2025-04-14",
    system_prompt="Come up with a descriptive filename for the following screenshot."
)

result = rename_file_agent.run_sync([BinaryContent(data=data, media_type="image/png")])

filename = result.output

class Category(BaseModel):
    category: str

category_agent = Agent(
    "openai:gpt-4.1-mini-2025-04-14",
    system_prompt="""You will get a list of categories and then you'll get a filename for a screenshot. 
        Decide if the screenshot belongs in an existing category or if a new category should be created for that screenshot. 
        And then return the category.""",
    output_type=Category
)

result = category_agent.run_sync(f"""
    Categories: {list_categories()}
    Filename: {filename}
""")

category = result.output.category

move_file_agent = Agent(
    "openai:gpt-4.1-mini-2025-04-14",
    system_prompt="You'll get a filename and a category. Use the tools to first create a category and then move the file to that category folder.",
    tools=[Tool(create_directory, takes_ctx=False), Tool(rename_and_move_screenshot, takes_ctx=False)]
)

move_file_agent.run_sync(
    f"Old filename: {newest_screenshot}\n" \
    f"New filename: {category}/{filename}\n" \
    f"Category: {category}"
)