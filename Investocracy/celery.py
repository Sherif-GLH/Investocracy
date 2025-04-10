import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Investocracy.settings')

## instnce of celery application ##
app = Celery('Investocracy')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()