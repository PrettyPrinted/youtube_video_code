import asyncio

from celery import shared_task
from pydantic_ai import Agent, ModelMessagesTypeAdapter
from sqlalchemy import select
from telegram import Bot
from flask import current_app
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIResponsesModel

from .models import Chat, Workout, Output
from .extensions import db

@shared_task
def process_workout_conversation(chat_id, message, thread_id=None):
    stmt = select(Chat).where(Chat.chat_id == chat_id).where(Chat.thread_id == thread_id)

    chat = db.session.scalars(stmt).first()
    history = None
    if chat:
        history = ModelMessagesTypeAdapter.validate_json(chat.data)
    else:
        chat = Chat(chat_id=chat_id, thread_id=thread_id)

    with open("prompts/track_workouts.md", "r") as f:
        instructions = f.read()

    model = OpenAIResponsesModel('gpt-5.4', provider=OpenAIProvider(api_key=current_app.config["OPENAI_API_KEY"]))
    agent = Agent(  
        output_type=Output,
        instructions=instructions,
        instrument=True,
    )
    result = agent.run_sync(message, message_history=history, model=model)
        
    chat.data = result.all_messages_json().decode()
    db.session.add(chat)
    db.session.commit()

    if result.output.to_follow_up:
        asyncio.run(send_telegram_chat(chat_id, result.output.follow_up, thread_id))
    else:
        for item in result.output.sets:
            workout = Workout(
                exercise = item.exercise,
                reps = item.reps,
                weight = item.weight
            )       
            db.session.add(workout)
        db.session.commit()

        asyncio.run(send_telegram_chat(chat_id, "Workout data saved!", thread_id))

async def send_telegram_chat(chat_id, text, thread_id=None):
    bot = Bot(token=current_app.config["TELEGRAM_API_KEY"])
    async with bot:
        await bot.send_message(chat_id=chat_id, text=text, message_thread_id=thread_id)