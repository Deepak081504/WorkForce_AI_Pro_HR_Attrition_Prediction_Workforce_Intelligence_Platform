from pydantic import BaseModel


class WorkforceSummary(BaseModel):
    total_employees: int
    active_employees: int
    inactive_employees: int

    total_departments: int

    present_today: int
    absent_today: int
    on_leave_today: int

    total_payroll_records: int
    total_payroll_amount: float

    pending_leave_requests: int
    approved_leave_requests: int
    rejected_leave_requests: int


class DepartmentAnalytics(BaseModel):
    department_id: int
    department_name: str
    employee_count: int


class AttendanceAnalytics(BaseModel):
    status: str
    count: int


class LeaveAnalytics(BaseModel):
    status: str
    count: int


class PayrollAnalytics(BaseModel):
    pay_period: str
    employee_count: int
    total_gross_salary: float
    total_net_salary: float