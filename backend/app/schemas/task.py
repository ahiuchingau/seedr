from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    # Seed-specific tasks
    HARVEST = "harvest"
    PRUNE = "prune"
    TRANSPLANT = "transplant"
    THIN_SEEDLINGS = "thin_seedlings"

    # Garden-specific tasks
    NUTRIENT_REFILL = "nutrient_refill"
    PH_CHECK = "ph_check"
    EC_CHECK = "ec_check"
    WATER_CHANGE = "water_change"
    CLEANING = "cleaning"
    FILTER_CHANGE = "filter_change"
    PUMP_MAINTENANCE = "pump_maintenance"
    TEMPERATURE_CHECK = "temperature_check"

    # General
    OTHER = "other"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    OVERDUE = "overdue"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskScope(str, Enum):
    """Defines what the task applies to"""
    SEED = "seed"  # Task for a specific seed batch
    GARDEN = "garden"  # Task for the entire garden system
    POD = "pod"  # Task for a specific pod


class Task(BaseModel):
    """Universal task model for both seed and garden tasks"""
    id: str
    task_type: TaskType
    scope: TaskScope
    title: str
    description: Optional[str] = None

    # References (one will be set based on scope)
    seed_batch_id: Optional[str] = None  # For seed-specific tasks
    garden_id: Optional[str] = None  # For garden-wide tasks
    pod_id: Optional[str] = None  # For pod-specific tasks

    # Scheduling
    scheduled_date: datetime
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

    # Status tracking
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM

    # Reminders
    reminder_sent: bool = False
    reminder_minutes_before: int = Field(
        default=60,
        description="Minutes before scheduled_date to send reminder"
    )

    # Recurrence
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # e.g., "daily", "weekly", "monthly"
    recurrence_interval: Optional[int] = None  # e.g., every 7 days

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "id": "task_harvest_001",
                    "task_type": "harvest",
                    "scope": "seed",
                    "title": "Harvest cherry tomatoes",
                    "seed_batch_id": "batch_001",
                    "scheduled_date": "2025-12-05T09:00:00Z",
                    "priority": "high",
                    "status": "pending"
                },
                {
                    "id": "task_refill_001",
                    "task_type": "nutrient_refill",
                    "scope": "garden",
                    "title": "Refill nutrient solution",
                    "description": "Add 500ml of nutrient solution A and B",
                    "garden_id": "garden_001",
                    "scheduled_date": "2025-10-10T09:00:00Z",
                    "priority": "medium",
                    "is_recurring": True,
                    "recurrence_pattern": "weekly",
                    "recurrence_interval": 7,
                    "status": "pending"
                }
            ]
        }


class Reminder(BaseModel):
    """Reminder for tasks or harvest dates"""
    id: str
    task_id: Optional[str] = None  # Reference to Task
    seed_batch_id: Optional[str] = None  # For harvest reminders
    reminder_type: str  # "task", "harvest", "custom"
    message: str
    scheduled_time: datetime
    sent: bool = False
    sent_at: Optional[datetime] = None

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "id": "reminder_001",
                    "task_id": "task_harvest_001",
                    "reminder_type": "task",
                    "message": "Cherry tomatoes ready for harvest in 1 hour",
                    "scheduled_time": "2025-12-05T08:00:00Z",
                    "sent": False
                },
                {
                    "id": "reminder_002",
                    "seed_batch_id": "batch_001",
                    "reminder_type": "harvest",
                    "message": "Cherry tomatoes estimated harvest in 3 days",
                    "scheduled_time": "2025-12-02T09:00:00Z",
                    "sent": False
                }
            ]
        }


# Request/Response schemas for API endpoints

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    task_type: TaskType
    scope: TaskScope
    title: str
    description: Optional[str] = None
    seed_batch_id: Optional[str] = None
    garden_id: Optional[str] = None
    pod_id: Optional[str] = None
    scheduled_date: datetime
    due_date: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    reminder_minutes_before: int = 60
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    notes: Optional[str] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    completed_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    notes: Optional[str] = None


class ReminderCreate(BaseModel):
    """Schema for creating a reminder"""
    task_id: Optional[str] = None
    seed_batch_id: Optional[str] = None
    reminder_type: str
    message: str
    scheduled_time: datetime
