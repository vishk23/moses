import os
import django
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

# Initialize Django to load settings
django.setup()

# Create the Celery app
app = Celery('django_app')
app.conf.broker_connection_retry_on_startup = True

# Load configuration from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all installed apps
app.autodiscover_tasks()