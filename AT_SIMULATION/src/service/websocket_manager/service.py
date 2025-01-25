import asyncio
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from fastapi.websockets import WebSocket

logger = logging.getLogger(__name__)


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
        self.connection_pool = _ConnectionPool()

    async def connect(self, websocket: WebSocket, user_id: int, process_id: str):
        await websocket.accept()
        self.connection_pool.add_connection(websocket, user_id, process_id)

    async def disconnect(self, user_id: int, process_id: str):
        self.connection_pool.remove_connection(user_id, process_id)

    async def send_message(self, message: str, user_id: int, process_id: str):
        connections = self.connection_pool.find_connections(user_id, process_id)
        for connection in connections:
            for websocket in connection.websockets:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message: {e}")

    async def broadcast(self, message: str):
        for connection in self.connection_pool.get_all_connections():
            for websocket in connection.websockets:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message: {e}")


@dataclass
class _Connection:
    user_id: int
    process_id: str
    websockets: List[WebSocket] = field(default_factory=list)


class _ConnectionPool:
    def __init__(self):
        self._connections: Dict[str, _Connection] = {}

    def _get_key(self, user_id: int, process_id: str) -> str:
        return f"{user_id}:{process_id}"

    def add_connection(self, websocket: WebSocket, user_id: int, process_id: str):
        key = self._get_key(user_id, process_id)
        if key not in self._connections:
            self._connections[key] = _Connection(user_id=user_id, process_id=process_id)
        self._connections[key].websockets.append(websocket)
        logger.info(f"Connection added for user {user_id} and process {process_id}")

    def remove_connection(self, user_id: int, process_id: str):
        key = self._get_key(user_id, process_id)
        if key in self._connections:
            connection = self._connections[key]
            for websocket in connection.websockets:
                try:
                    asyncio.create_task(websocket.close())
                except Exception as e:
                    logger.error(f"Error closing websocket: {e}")
            del self._connections[key]
            logger.info(
                f"Connection removed for user {user_id} and process {process_id}"
            )

    def find_connections(
        self, user_id: Optional[int] = None, process_id: Optional[str] = None
    ) -> List[_Connection]:
        if user_id is None and process_id is None:
            return list(self._connections.values())

        result = []
        for key, connection in self._connections.items():
            if (user_id is None or connection.user_id == user_id) and (
                process_id is None or connection.process_id == process_id
            ):
                result.append(connection)
        return result

    def get_all_connections(self) -> List[_Connection]:
        return list(self._connections.values())


def get_websocket_manager() -> WebsocketManager:
    return WebsocketManager()
