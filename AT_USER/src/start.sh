#!/bin/bash

# Run Alembic migrations
alembic upgrade head

# Check if debugpy is installed
if [ "$DEBUG" = "true" ]; then
    if ! python -c "import debugpy" &> /dev/null; then
        echo "debugpy is not installed. Installing debugpy..."
        pip install debugpy
    fi

    # Start the FastAPI app with debugpy
    python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn src.application:app --host 0.0.0.0 --port $SERVER_PORT
else
    # Start the FastAPI app without debugpy
    python -Xfrozen_modules=off -m uvicorn src.application:app --host 0.0.0.0 --port $SERVER_PORT
fi
