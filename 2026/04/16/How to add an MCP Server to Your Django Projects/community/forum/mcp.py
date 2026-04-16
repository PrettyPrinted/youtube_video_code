from mcp_server import MCPToolset
from .services import *

class ForumTools(MCPToolset):
    def get_threads(self) -> list[dict]:
        threads = get_threads_service()
        return [
            {
                "id": thread.id,
                "title": thread.title,
                "description": thread.description,
                "date_created": str(thread.date_created),
            }
            for thread in threads
        ]

    def create_thread(self, title: str, content: str) -> dict:
        thread = create_threads_service(title, content)
        return {
            "id": thread.id,
            "title": thread.title,
            "description": thread.description,
            "date_created": str(thread.date_created),
        }
    
    def add_reply(self, thread_id: int, message: str) -> dict:
        reply = create_replies_service(thread_id, message, self.request.user)
        return {
            "id": reply.id,
            "content": reply.message,
            "date_created": str(reply.date_created),
        }