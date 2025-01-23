import asyncio
from typing import Dict, List, Optional
from fastapi.websockets import WebSocket


class WebsocketManager:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:

            async def initialize():
                async with cls._lock:
                    if not cls._instance:
                        cls._instance = super(WebsocketManager, cls).__new__(
                            cls, *args, **kwargs
                        )
                        cls._instance._initialize()

            asyncio.run(initialize())
        return cls._instance

    def _initialize(self):
        self.active_connections: Dict[int, Dict[str, Optional[WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, process_id: str):
        if (
            user_id in self.active_connections
            and process_id in self.active_connections[user_id]
            and self.active_connections[user_id][process_id] is not None
        ):
            print(
                f"Connection already exists for user {user_id} and process {process_id}. Closing new connection."
            )
            await websocket.close(
                code=1000, reason="Only one connection allowed per user and process."
            )
            return

        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}

        self.active_connections[user_id][process_id] = websocket

        print(f"Websocket connected for user {user_id} and process {process_id}")

    async def disconnect(self, user_id: int, process_id: str):
        if (
            user_id in self.active_connections
            and process_id in self.active_connections[user_id]
        ):
            websocket = self.active_connections[user_id][process_id]
            if websocket:
                try:
                    await websocket.close()
                except RuntimeError as e:
                    print(f"Error closing websocket: {e}")
                except Exception as e:
                    print(f"Unexpected error closing websocket: {e}")
            self.active_connections[user_id][process_id] = None  #
            print(f"Websocket disconnected for user {user_id} and process {process_id}")

            if all(
                value is None for value in self.active_connections[user_id].values()
            ):
                del self.active_connections[user_id]

    async def send_message(self, message: str, user_id: int, process_id: str):
        if (
            user_id in self.active_connections
            and process_id in self.active_connections[user_id]
        ):
            websocket = self.active_connections[user_id][process_id]
            if websocket:
                try:
                    await websocket.send_text(message)
                except RuntimeError as e:
                    print(f"Error sending message: {e}")
                except Exception as e:
                    print(f"Unexpected error sending message: {e}")

    async def broadcast(self, message: str):
        for user_connections in self.active_connections.values():
            for websocket in user_connections.values():
                if websocket:
                    try:
                        await websocket.send_text(message)
                    except RuntimeError as e:
                        print(f"Error sending message: {e}")
                    except Exception as e:
                        print(f"Unexpected error sending message: {e}")


def get_websocket_manager() -> WebsocketManager:
    return WebsocketManager()
