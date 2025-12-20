web: gunicorn stream_sentry.wsgi:application --log-file -
worker: celery -A stream_sentry worker --loglevel=info
