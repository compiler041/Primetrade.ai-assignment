#!/bin/bash
set -e

echo "Waiting for postgres..."
while ! pg_isready -h postgres -p 5432 -U postgres; do
  sleep 1
done
echo "Postgres is ready!"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Loading initial data..."
python -m app.initial_data

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
