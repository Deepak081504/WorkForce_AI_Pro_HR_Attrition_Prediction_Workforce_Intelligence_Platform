from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field


class AttendanceCreate(BaseModel):
    employee_id: int
    shift_id: int | None = None
    attendance_date: date

    check_in: time | None = None
    check_out: time | None = None

    status: str = Field(
        default="PRESENT",
        max_length=30,
    )

    remarks: str | None = Field(
        default=None,
        max_length=255,
    )


class AttendanceUpdate(BaseModel):
    shift_id: int | None = None
    check_in: time | None = None
    check_out: time | None = None
    status: str | None = None
    remarks: str | None = None


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    shift_id: int | None

    attendance_date: date
    check_in: time | None
    check_out: time | None

    status: str
    remarks: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )