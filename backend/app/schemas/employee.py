from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):
    employee_code: str = Field(min_length=2, max_length=50)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    date_of_birth: date | None = None
    joining_date: date

    designation: str = Field(
        min_length=2,
        max_length=100,
    )

    department_id: int | None = None
    manager_id: int | None = None

    status: str = "ACTIVE"


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    email: EmailStr | None = None
    phone: str | None = None

    date_of_birth: date | None = None
    joining_date: date | None = None

    designation: str | None = None
    department_id: int | None = None
    manager_id: int | None = None

    status: str | None = None


class EmployeeResponse(BaseModel):
    id: int
    employee_code: str

    first_name: str
    last_name: str

    email: EmailStr
    phone: str | None

    date_of_birth: date | None
    joining_date: date

    designation: str

    department_id: int | None
    manager_id: int | None

    status: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)