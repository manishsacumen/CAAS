import os

from celery import Celery

from Connector.schedule import send_scheduled_alert


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CaaS.settings')

app = Celery('CaaS')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(86400.0, send_scheduled_alert.s())