from ninja import ModelSchema

from .models import Garden, GardenEnvironmentLog, GardenPod


class GardenSchema(ModelSchema):
    """Schema for creating or updating a garden"""

    class Meta:
        model = Garden
        exclude = ["id", "created_at", "updated_at"]


class PodSchema(ModelSchema):
    """Schema for creating a new pod"""

    class Meta:
        model = GardenPod
        exclude = ["id", "created_at", "updated_at"]


class GardenEnvironmentSchema(ModelSchema):
    """Schema for creating an environment log entry"""

    class Meta:
        model = GardenEnvironmentLog
        exclude = ["id", "timestamp"]
