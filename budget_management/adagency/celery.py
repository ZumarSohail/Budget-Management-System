import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adagency.settings')

app = Celery('adagency')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'check-budgets-every-5-min': {
        'task': 'campaigns.tasks.check_budgets_and_schedules',
        'schedule': 300.0,
    },
    'reset-daily-spends': {
        'task': 'campaigns.tasks.reset_daily_spends',
        'schedule': 86400.0,
    },
    'reset-monthly-spends': {
        'task': 'campaigns.tasks.reset_monthly_spends',
        'schedule': 2592000.0,
    },
}