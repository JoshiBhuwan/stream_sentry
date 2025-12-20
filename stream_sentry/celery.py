import os
from celery import Celery

# Set standard Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stream_sentry.settings')

app = Celery('stream_sentry')

# Load configuration from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
