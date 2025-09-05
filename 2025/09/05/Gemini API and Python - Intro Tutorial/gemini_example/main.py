from google import genai
from google.genai import types

client = genai.Client()

uploaded_file = client.files.upload(file="cat.jpg")

def get_current_weather(location: str) -> str:
    """Returns the current weather

    Args:
     location: the city and state, for example: Los Angeles, CA
    """
    return "snowy"

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    #contents=["what do you see in this image?", uploaded_file],
    contents="what's the weather like in miami, florida?",
    config=types.GenerateContentConfig(
        #system_instruction="You are a rude teacher"
        tools=[get_current_weather]
    )
)

print(response.text)