from .models import Brand, Campaign
from django.db import transaction
from typing import Tuple, Literal

BudgetType = Literal['daily', 'monthly']

def record_spend(campaign: Campaign, amount: float) -> None:
    with transaction.atomic():
        brand = Brand.objects.select_for_update().get(id=campaign.brand.id)
        brand.daily_spend += amount
        brand.monthly_spend += amount
        brand.save()
        check_budget_status(brand)

def check_budget_status(brand: Brand) -> Tuple[bool, bool]:
    daily_exceeded = brand.daily_spend >= brand.daily_budget
    monthly_exceeded = brand.monthly_spend >= brand.monthly_budget
    return daily_exceeded, monthly_exceeded

def enforce_campaign_status() -> None:
    for brand in Brand.objects.prefetch_related('campaigns'):
        daily_exceeded, monthly_exceeded = check_budget_status(brand)
        for campaign in brand.campaigns.all():
            should_be_active = True
            if daily_exceeded or monthly_exceeded:
                should_be_active = False
            if should_be_active and not campaign.is_within_schedule():
                should_be_active = False
            if should_be_active and campaign.status != Campaign.Status.ACTIVE:
                campaign.status = Campaign.Status.ACTIVE
                campaign.save()
            elif not should_be_active and campaign.status != Campaign.Status.PAUSED:
                campaign.status = Campaign.Status.PAUSED
                campaign.save()