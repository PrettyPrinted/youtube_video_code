from celery import shared_task
from openai import OpenAI

from .models import Image

@shared_task
def generate_image(prompt):
    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    Image.objects.create(url=response.data[0].url, prompt=prompt)