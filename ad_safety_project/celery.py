import os
from celery import Celery

# Set standard Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ad_safety_project.settings')

app = Celery('ad_safety_project')

# Load configuration from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
