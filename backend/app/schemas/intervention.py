from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InterventionCreate(BaseModel):
    employee_id: int

    intervention_type: str = Field(
        min_length=2,
        max_length=50,
    )

    recommendation: str = Field(
        min_length=5,
        max_length=2000,
    )

    priority: str = Field(
        default="MEDIUM",
        max_length=20,
    )

    notes: str | None = Field(
        default=None,
        max_length=2000,
    )


class InterventionUpdate(BaseModel):
    priority: str | None = Field(
        default=None,
        max_length=20,
    )

    status: str | None = Field(
        default=None,
        max_length=30,
    )

    notes: str | None = Field(
        default=None,
        max_length=2000,
    )


class InterventionResponse(BaseModel):
    id: int
    employee_id: int
    risk_level: str
    intervention_type: str
    recommendation: str
    priority: str
    status: str
    notes: str | None
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )