from datetime import datetime
from typing import Optional

from django.db import models


class PodStatus(models.IntegerChoices):
    EMPTY = 0
    PLANTED = 1
    GROWING = 2
    HARVESTING = 3
    MAINTENANCE = 4


class Garden(models.Model):
    """Hydroponic garden system configuration"""

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    total_pods = models.PositiveIntegerField()

    location = models.CharField(max_length=100, null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class GardenPod(models.Model):
    """Individual growing pod in a garden"""

    pod_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100, null=True, blank=True)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="pods")
    status = models.IntegerField(choices=PodStatus, default=PodStatus.EMPTY)

    # Seed assignment
    seed_batch_id: Optional[str] = None  # Reference to SeedBatch if planted

    # Planting info
    planted_date: Optional[datetime] = None

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Pod {self.pod_number} in {self.garden.name}"


class GardenEnvironmentLog(models.Model):
    """Environmental measurements for the entire garden system"""

    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="environment_logs")
    timestamp = models.DateTimeField(auto_now_add=True)

    # Water quality
    ph_level = models.FloatField(null=True, blank=True)
    ec_level = models.FloatField(null=True, blank=True)
    water_temp_c = models.FloatField(null=True, blank=True)
    dissolved_oxygen = models.FloatField(null=True, blank=True)

    # Ambient conditions
    air_temp_c = models.FloatField(null=True, blank=True)
    humidity_percent = models.FloatField(null=True, blank=True)
    light_intensity_lux = models.IntegerField(null=True, blank=True)

    # Notes
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Env Log for {self.garden.name} at {self.timestamp}"
