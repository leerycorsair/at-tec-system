import asyncio
from typing import Dict, List
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
        self.active_connections: Dict[int, Dict[int, List[WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, process_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
        if process_id not in self.active_connections[user_id]:
            self.active_connections[user_id][process_id] = []
        self.active_connections[user_id][process_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int, process_id: int):
        if user_id in self.active_connections:
            if process_id in self.active_connections[user_id]:
                self.active_connections[user_id][process_id].remove(websocket)
                if not self.active_connections[user_id][process_id]:
                    del self.active_connections[user_id][process_id]
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_message(self, message: str, user_id: int, process_id: int):
        if (
            user_id in self.active_connections
            and process_id in self.active_connections[user_id]
        ):
            for websocket in self.active_connections[user_id][process_id]:
                await websocket.send_text(message)

    async def broadcast(self, message: str):
        for _, processes in self.active_connections.items():
            for _, websockets in processes.items():
                for websocket in websockets:
                    await websocket.send_text(message)


def get_websocket_manager() -> WebsocketManager:
    return WebsocketManager()
