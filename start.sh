#!/bin/bash

# Exit on error
set -o errexit

# Apply Migrations
echo "Applying database migrations..."
python manage.py migrate

# Start RabbitMQ Server in the background (using & to keep logs attached to stdout)
echo "Starting RabbitMQ..."
rabbitmq-server &
# Wait for RabbitMQ to be ready
echo "Waiting for RabbitMQ to launch on 5672..."
TIMEOUT=60
COUNTER=0
while ! nc -z localhost 5672; do   
  sleep 1
  COUNTER=$((COUNTER+1))
  echo "Waiting for RabbitMQ... ($COUNTER/$TIMEOUT)"
  if [ $COUNTER -ge $TIMEOUT ]; then
      echo "RabbitMQ failed to start within $TIMEOUT seconds."
      exit 1
  fi
done
echo "RabbitMQ started!"

# Start Redis Server in the background
echo "Starting Redis..."
redis-server --port 6379 --bind 127.0.0.1 --daemonize yes

# Start Celery in the background
echo "Starting Celery Worker..."
celery -A stream_sentry worker --loglevel=info --concurrency 2 &

# Start Gunicorn in the foreground
echo "Starting Gunicorn Web Server..."
exec gunicorn stream_sentry.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 8 --timeout 0
