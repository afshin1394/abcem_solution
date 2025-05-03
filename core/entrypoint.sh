#!/bin/sh
set -e

echo "Waiting for Postgres to become ready..."

# Loop until Postgres is ready to accept connections
until pg_isready -h "postgres" -p "5432" -U "dev_user"; do
    echo "postgres 5432 dev_user"
    echo "Postgres is unavailable - sleeping"
    sleep 2
done

echo "Postgres is up - running migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8001


