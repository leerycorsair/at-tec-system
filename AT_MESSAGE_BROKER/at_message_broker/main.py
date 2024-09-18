from at_queue.core.session import ConnectionParameters
from at_queue.core.at_registry import ATRegistry
import asyncio


async def main():
    connection_parameters = ConnectionParameters("amqp://localhost:5672/")
    registry = ATRegistry(connection_parameters)
    await registry.initialize()
    await registry.start()


if __name__ == "__main__":
    asyncio.run(main())
