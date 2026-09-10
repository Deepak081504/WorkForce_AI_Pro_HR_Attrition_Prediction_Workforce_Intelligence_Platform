from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class LeaveTypeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(
        default=None,
        max_length=255,
    )
    total_days: int = Field(
        default=12,
        ge=1,
        le=365,
    )


class LeaveTypeUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=255,
    )
    total_days: int | None = Field(
        default=None,
        ge=1,
        le=365,
    )


class LeaveTypeResponse(BaseModel):
    id: int
    name: str
    description: str | None
    total_days: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str | None = Field(
        default=None,
        max_length=500,
    )


class LeaveRequestUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = None


class LeaveStatusUpdate(BaseModel):
    status: str = Field(
        min_length=2,
        max_length=30,
    )


class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str | None
    status: str
    approved_by: int | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )