from typing import Optional, Union
from yarl import URL
import os
from dataclasses import dataclass


@dataclass
class RabbitMQConfig:
    host: str
    port: int
    login: str
    password: str
    virtualhost: str
    ssl: bool
    url: URL


class RabbitMQStore:
    @classmethod
    def get_rabbitmq_config(cls) -> RabbitMQConfig:
        RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
        RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
        RABBITMQ_LOGIN = os.getenv("RABBITMQ_LOGIN", "guest")
        RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
        RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
        RABBITMQ_SSL = bool(os.getenv("RABBITMQ_SSL", False))

        scheme = "amqps" if RABBITMQ_SSL else "amqp"
        RABBITMQ_URL = URL.build(
            scheme=scheme,
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            user=RABBITMQ_LOGIN,
            password=RABBITMQ_PASSWORD,
            path=RABBITMQ_VHOST,
        )

        return RabbitMQConfig(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            login=RABBITMQ_LOGIN,
            password=RABBITMQ_PASSWORD,
            virtualhost=RABBITMQ_VHOST,
            ssl=RABBITMQ_SSL,
            url=RABBITMQ_URL,
        )
