#!/bin/sh

# Exit on any error
set -e

# Print commands for debugging
set -x

# Maximum wait time (in seconds)
MAX_WAIT=60
COUNTER=0

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  COUNTER=$((COUNTER+1))
  if [ $COUNTER -gt $MAX_WAIT ]; then
    echo "Timeout waiting for PostgreSQL"
    exit 1
  fi
  echo "Waiting for PostgreSQL... (${COUNTER}s)"
  sleep 1
done

echo "PostgreSQL is up - initializing database"
python -c "from app.initial_data import run_init_db; run_init_db()"

echo "Starting FastAPI application"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
