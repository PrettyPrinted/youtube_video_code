from celery import shared_task
from openai import OpenAI

from .extensions import db
from .models import Images

@shared_task
def generate_image(prompt):
    client = OpenAI()

    image = Images(url="https://placehold.co/1024x1024", prompt=prompt)
    db.session.add(image)
    db.session.commit()

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image.url = response.data[0].url
    db.session.commit()

