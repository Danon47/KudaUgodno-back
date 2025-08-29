import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_queues = {
    "emails": {
        "exchange": "emails",
        "routing_key": "emails",
    },
    "default": {
        "exchange": "default",
        "routing_key": "default",
    },
}

app.conf.task_default_queue = "default"
app.conf.task_default_exchange = "default"
app.conf.task_default_routing_key = "default"

app.autodiscover_tasks()
