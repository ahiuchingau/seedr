from datetime import datetime, date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class SeedType(str, Enum):
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    HERB = "herb"
    FLOWER = "flower"
    OTHER = "other"


class GrowthStage(str, Enum):
    GERMINATION = "germination"
    SEEDLING = "seedling"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    FRUITING = "fruiting"
    HARVEST_READY = "harvest_ready"
    HARVESTED = "harvested"


class Seed(BaseModel):
    """Seed information - the variety and its characteristics"""

    id: str
    name: str  # e.g., "Cherry Tomato", "Basil"
    seed_type: SeedType
    variety: Optional[str] = None  # e.g., "Sweet 100", "Genovese"
    supplier: Optional[str] = None

    # Growth characteristics
    germination_days: int = Field(default=7, description="Expected days for germination")
    days_to_harvest: int = Field(
        default=60, description="Expected days from germination to harvest"
    )

    # Optional growing information
    optimal_ph_min: Optional[float] = None
    optimal_ph_max: Optional[float] = None
    optimal_ec_min: Optional[float] = None
    optimal_ec_max: Optional[float] = None
    optimal_temp_c_min: Optional[float] = None
    optimal_temp_c_max: Optional[float] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "seed_tomato_001",
                "name": "Cherry Tomato",
                "seed_type": "vegetable",
                "variety": "Sweet 100",
                "supplier": "Burpee Seeds",
                "germination_days": 7,
                "days_to_harvest": 65,
                "optimal_ph_min": 5.5,
                "optimal_ph_max": 6.5,
            }
        }


class SeedBatch(BaseModel):
    """A batch of seeds planted - links seed variety to actual planting"""

    id: str
    seed_id: str  # Reference to Seed
    batch_number: Optional[str] = None

    # Planting tracking
    germination_start_date: date
    actual_germination_date: Optional[date] = None

    # Growth tracking
    current_stage: GrowthStage = GrowthStage.GERMINATION
    predicted_harvest_date: Optional[date] = None
    actual_harvest_date: Optional[date] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "batch_001",
                "seed_id": "seed_tomato_001",
                "batch_number": "BATCH-2025-001",
                "germination_start_date": "2025-10-01",
                "current_stage": "germination",
            }
        }


class GrowthLogEntry(BaseModel):
    """Individual growth observation or measurement for a seed batch"""

    id: str
    seed_batch_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Observations
    observation: Optional[str] = None
    height_cm: Optional[float] = None
    leaf_count: Optional[int] = None

    # Photos
    photo_urls: list[str] = Field(default_factory=list)
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "log_001",
                "seed_batch_id": "batch_001",
                "timestamp": "2025-10-05T10:30:00Z",
                "observation": "First true leaves emerging",
                "height_cm": 5.2,
                "leaf_count": 4,
            }
        }


# Request/Response schemas for API endpoints


class SeedCreate(BaseModel):
    """Schema for creating a new seed variety"""

    name: str
    seed_type: SeedType
    variety: Optional[str] = None
    supplier: Optional[str] = None
    germination_days: int = 7
    days_to_harvest: int = 60
    optimal_ph_min: Optional[float] = None
    optimal_ph_max: Optional[float] = None
    optimal_ec_min: Optional[float] = None
    optimal_ec_max: Optional[float] = None
    optimal_temp_c_min: Optional[float] = None
    optimal_temp_c_max: Optional[float] = None
    notes: Optional[str] = None


class SeedUpdate(BaseModel):
    """Schema for updating a seed variety"""

    name: Optional[str] = None
    variety: Optional[str] = None
    supplier: Optional[str] = None
    germination_days: Optional[int] = None
    days_to_harvest: Optional[int] = None
    optimal_ph_min: Optional[float] = None
    optimal_ph_max: Optional[float] = None
    optimal_ec_min: Optional[float] = None
    optimal_ec_max: Optional[float] = None
    optimal_temp_c_min: Optional[float] = None
    optimal_temp_c_max: Optional[float] = None
    notes: Optional[str] = None


class SeedBatchCreate(BaseModel):
    """Schema for creating a new seed batch"""

    seed_id: str
    batch_number: Optional[str] = None
    germination_start_date: date
    notes: Optional[str] = None


class SeedBatchUpdate(BaseModel):
    """Schema for updating a seed batch"""

    current_stage: Optional[GrowthStage] = None
    actual_germination_date: Optional[date] = None
    actual_harvest_date: Optional[date] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class GrowthLogCreate(BaseModel):
    """Schema for adding a growth log entry"""

    observation: Optional[str] = None
    height_cm: Optional[float] = None
    leaf_count: Optional[int] = None
    photo_urls: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
