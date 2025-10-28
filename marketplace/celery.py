# =================================================================================

from __future__ import absolute_import
from celery.schedules import crontab
from celery import Celery
import os

# =================================================================================


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
app = Celery('marketplace')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Agenda diária de reposição automática de estoque
app.conf.beat_schedule = {
    "repor_estoque_cron": {
        "task": "apps.estoque.tasks.repor_estoque",
        "schedule": crontab(hour=0, minute=0),
    },
}

# =================================================================================
