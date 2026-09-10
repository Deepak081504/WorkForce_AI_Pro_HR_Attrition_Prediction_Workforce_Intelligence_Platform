from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PayrollCreate(BaseModel):
    employee_id: int
    pay_period: str = Field(
        min_length=3,
        max_length=20,
    )
    pay_date: date

    basic_salary: float = Field(
        ge=0
    )

    allowances: float = Field(
        default=0,
        ge=0,
    )

    deductions: float = Field(
        default=0,
        ge=0,
    )

    bonus: float = Field(
        default=0,
        ge=0,
    )

    status: str = "PENDING"


class PayrollUpdate(BaseModel):
    pay_period: str | None = Field(
        default=None,
        max_length=20,
    )

    pay_date: date | None = None

    basic_salary: float | None = Field(
        default=None,
        ge=0,
    )

    allowances: float | None = Field(
        default=None,
        ge=0,
    )

    deductions: float | None = Field(
        default=None,
        ge=0,
    )

    bonus: float | None = Field(
        default=None,
        ge=0,
    )

    status: str | None = None


class PayrollResponse(BaseModel):
    id: int
    employee_id: int
    pay_period: str
    pay_date: date

    basic_salary: float
    allowances: float
    deductions: float
    bonus: float

    gross_salary: float
    net_salary: float

    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )