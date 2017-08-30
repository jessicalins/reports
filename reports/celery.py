from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from reports import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reports.settings')

app = Celery('reports')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'process-reports-nightly': {
        'task': 'reportsapp.tasks.report_processing',
        'schedule': crontab(minute=30, hour=4)
    },
}
