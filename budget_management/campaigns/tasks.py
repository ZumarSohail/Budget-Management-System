from celery import shared_task
from .logic import enforce_campaign_status
from .models import Brand
from datetime import datetime
from typing import Final

RESET_HOUR: Final[int] = 0

@shared_task
def check_budgets_and_schedules() -> None:
    enforce_campaign_status()

@shared_task
def reset_daily_spends() -> None:
    Brand.objects.update(daily_spend=0)
    check_budgets_and_schedules.delay()

@shared_task
def reset_monthly_spends() -> None:
    if datetime.utcnow().day == 1:
        Brand.objects.update(monthly_spend=0)
        check_budgets_and_schedules.delay()