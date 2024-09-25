#!/bin/bash

echo "Starting migration script..."

ENV_PATH="./docker/at_user_local/.env"
DOCKER_COMPOSE_PATH="./docker/at_user_local/docker-compose.yml"

if [ -z "$1" ]; then
  echo "No revision name provided. Usage: $0 <revision_name>"
  exit 1
fi

REVISION_NAME=$1

echo "Starting PostgreSQL container..."
docker-compose -f $DOCKER_COMPOSE_PATH up -d postgres_user
if [ $? -ne 0 ]; then
  echo "Failed to start PostgreSQL container."
  exit 1
fi

if [ ! -f $ENV_PATH ]; then
  echo ".env file not found at $ENV_PATH."
  exit 1
fi

ORIGINAL_HOST=$(grep DB_HOST $ENV_PATH | cut -d '=' -f2)

sed -i 's/DB_HOST=.*/DB_HOST=localhost/' $ENV_PATH

set -o allexport
. $ENV_PATH
set +o allexport

echo "Running Alembic revision..."
poetry run alembic revision --autogenerate -m "$REVISION_NAME"
REVISION_EXIT_CODE=$?

if [ $REVISION_EXIT_CODE -ne 0 ]; then
  echo "Alembic revision command failed. Exiting..."
  exit $REVISION_EXIT_CODE
fi

unset DB_HOST DB_PORT DB_NAME DB_USER DB_PASS SERVER_PORT

echo "Stopping PostgreSQL container..."
docker-compose -f $DOCKER_COMPOSE_PATH down postgres_user
if [ $? -ne 0 ]; then
  echo "Failed to stop PostgreSQL container."
  exit 1
fi

sed -i "s/DB_HOST=.*/DB_HOST=${ORIGINAL_HOST}/" $ENV_PATH

echo "Pipeline completed."