from flask import Blueprint, request
from .tasks import process_workout_conversation

main = Blueprint("main", "__name__")

@main.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    process_workout_conversation.delay(data["chat_id"], data["message"], data["thread_id"])
    return {}