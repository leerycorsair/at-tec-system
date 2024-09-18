#!/bin/bash

alembic upgrade head

uvicorn src.application:app --host 0.0.0.0 --port $SERVER_PORT
