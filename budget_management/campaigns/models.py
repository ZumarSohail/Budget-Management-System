
# Create your models here.
from django.db import models
from django.utils import timezone
from typing import TypedDict, List, Literal

class ScheduleConfig(TypedDict):
    days: List[Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]]
    start_time: str
    end_time: str

class Brand(models.Model):
    name = models.CharField(max_length=255)
    daily_budget = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2)
    daily_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)

class Campaign(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    schedule = models.JSONField(blank=True, null=True)
    
    def is_within_schedule(self) -> bool:
        from datetime import datetime
        now = datetime.now()
        if not self.schedule:
            return True
        config: ScheduleConfig = self.schedule
        current_day = now.strftime("%a").lower()[:3]
        if current_day not in config['days']:
            return False
        current_time = now.strftime("%H:%M")
        return config['start_time'] <= current_time <= config['end_time']