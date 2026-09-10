from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    assigned_to: int

    priority: str = Field(
        default="MEDIUM",
        max_length=20,
    )

    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    assigned_to: int | None = None

    priority: str | None = Field(
        default=None,
        max_length=20,
    )

    status: str | None = Field(
        default=None,
        max_length=30,
    )

    due_date: date | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    assigned_to: int
    created_by: int
    priority: str
    status: str
    due_date: date | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )