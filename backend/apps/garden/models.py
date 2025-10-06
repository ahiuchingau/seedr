from datetime import datetime
from typing import Optional
from enum import StrEnum
from ninja import Schema, Field


class PodStatus(StrEnum):
    EMPTY = "empty"
    PLANTED = "planted"
    GROWING = "growing"
    HARVESTING = "harvesting"
    MAINTENANCE = "maintenance"


class Garden(Schema):
    """Hydroponic garden system configuration"""

    id: str
    name: str
    description: Optional[str] = None
    total_pods: int = Field(gt=0, description="Total number of growing pods in the garden")

    # System configuration
    system_type: Optional[str] = None  # e.g., "NFT", "DWC", "Ebb & Flow"
    location: Optional[str] = None

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    is_active: bool = True
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "garden_001",
                "name": "Indoor Hydro System",
                "description": "Main hydroponic garden in the kitchen",
                "total_pods": 12,
                "system_type": "NFT",
                "location": "Kitchen",
            }
        }


class Pod(Schema):
    """Individual growing pod in a garden"""

    id: str
    garden_id: str
    pod_number: int = Field(ge=1, description="Pod position number in the garden")
    status: PodStatus = PodStatus.EMPTY

    # Seed assignment
    seed_batch_id: Optional[str] = None  # Reference to SeedBatch if planted

    # Planting info
    planted_date: Optional[datetime] = None

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "pod_001",
                "garden_id": "garden_001",
                "pod_number": 1,
                "status": "planted",
                "seed_batch_id": "batch_001",
                "planted_date": "2025-10-01T10:00:00Z",
            }
        }


class GardenEnvironmentLog(Schema):
    """Environmental measurements for the entire garden system"""

    id: str
    garden_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))

    # Water quality
    ph_level: Optional[float] = None
    ec_level: Optional[float] = None
    water_temp_c: Optional[float] = None
    dissolved_oxygen: Optional[float] = None

    # Ambient conditions
    air_temp_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    light_intensity_lux: Optional[int] = None

    # Notes
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "env_log_001",
                "garden_id": "garden_001",
                "timestamp": "2025-10-05T14:30:00Z",
                "ph_level": 6.2,
                "ec_level": 1.8,
                "water_temp_c": 22.5,
                "air_temp_c": 24.0,
                "humidity_percent": 65.0,
            }
        }


# Request/Response schemas for API endpoints


class GardenCreate(Schema):
    """Schema for creating a new garden"""

    name: str
    description: Optional[str] = None
    total_pods: int = Field(gt=0)
    system_type: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class GardenUpdate(Schema):
    """Schema for updating a garden"""

    name: Optional[str] = None
    description: Optional[str] = None
    system_type: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class PodCreate(Schema):
    """Schema for creating a new pod"""

    garden_id: str
    pod_number: int = Field(ge=1)
    notes: Optional[str] = None


class PodUpdate(Schema):
    """Schema for updating a pod"""

    status: Optional[PodStatus] = None
    seed_batch_id: Optional[str] = None
    planted_date: Optional[datetime] = None
    notes: Optional[str] = None


class GardenEnvironmentLogCreate(Schema):
    """Schema for creating an environment log entry"""

    ph_level: Optional[float] = None
    ec_level: Optional[float] = None
    water_temp_c: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    air_temp_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    light_intensity_lux: Optional[int] = None
    notes: Optional[str] = None
