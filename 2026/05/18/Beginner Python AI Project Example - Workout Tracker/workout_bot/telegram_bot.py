import httpx
import logging
import os

from dotenv import load_dotenv
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

async def handle_text_message(update, context):
    async with httpx.AsyncClient() as client:
        await client.post(f'{os.environ.get("API_BASE_URL")}/api', 
            json={
                "chat_id": update.effective_chat.id, 
                "message": update.message.text, 
                "thread_id": update.message.message_thread_id}
        )

async def unknown(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_API_KEY")).build()
    
    start_handler = CommandHandler('start', start)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(unknown_handler)
    
    application.run_polling()