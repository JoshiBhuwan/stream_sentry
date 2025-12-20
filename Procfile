web: gunicorn ad_safety_project.wsgi:application --log-file -
worker: celery -A ad_safety_project worker --loglevel=info
