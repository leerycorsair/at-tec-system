#!/bin/bash

echo "Starting Alembic downgrade script..."

ENV_PATH="./docker/at_user_local/.env"
DOCKER_COMPOSE_PATH="./docker/at_user_local/docker-compose.yml"

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

echo "Running Alembic downgrade by one revision..."
poetry run alembic downgrade -1
DOWNGRADE_EXIT_CODE=$?

if [ $DOWNGRADE_EXIT_CODE -ne 0 ]; then
  echo "Alembic downgrade command failed. Exiting..."
  exit $DOWNGRADE_EXIT_CODE
fi

unset DB_HOST DB_PORT DB_NAME DB_USER DB_PASS SERVER_PORT

echo "Stopping PostgreSQL container..."
docker-compose -f $DOCKER_COMPOSE_PATH down postgres_user
if [ $? -ne 0 ]; then
  echo "Failed to stop PostgreSQL container."
  exit 1
fi

sed -i "s/DB_HOST=.*/DB_HOST=${ORIGINAL_HOST}/" $ENV_PATH

echo "Downgrade pipeline completed successfully."