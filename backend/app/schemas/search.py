from pydantic import BaseModel


class EmployeeSearchResponse(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: str
    email: str
    designation: str
    department_id: int | None
    status: str


class DepartmentSearchResponse(BaseModel):
    id: int
    name: str
    description: str | None


class AttendanceSearchResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: str
    status: str
    shift_id: int | None


class LeaveSearchResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: str
    end_date: str
    status: str


class PayrollSearchResponse(BaseModel):
    id: int
    employee_id: int
    pay_period: str
    status: str
    net_salary: float


class PerformanceReviewSearchResponse(BaseModel):
    id: int
    employee_id: int
    review_period: str
    rating: float | None
    status: str