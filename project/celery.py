import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.conf.broker_url = 'redis://localhost:6379/0'
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)



app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'apps.core.tasks.dump_db',
        'schedule': crontab(hour=4, minute=00, day_of_week=1),
        # 'args': (16, 16),
    },
}
app.conf.timezone = 'Europe/Moscow'