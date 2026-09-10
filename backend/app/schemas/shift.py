from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field


class ShiftCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    start_time: time
    end_time: time

    description: str | None = Field(
        default=None,
        max_length=255,
    )


class ShiftUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    start_time: time | None = None
    end_time: time | None = None

    description: str | None = Field(
        default=None,
        max_length=255,
    )


class ShiftResponse(BaseModel):
    id: int
    name: str
    start_time: time
    end_time: time
    description: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )