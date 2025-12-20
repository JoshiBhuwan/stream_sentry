#!/bin/bash

# Exit on error
set -o errexit

# Apply Migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Celery in the background
echo "Starting Celery Worker..."
celery -A stream_sentry worker --loglevel=info --concurrency 2 &

# Start Gunicorn in the foreground
echo "Starting Gunicorn Web Server..."
gunicorn stream_sentry.wsgi:application --bind 0.0.0.0:$PORT
