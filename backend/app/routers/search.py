from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.attendance import Attendance
from app.models.department import Department
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest
from app.models.payroll import Payroll
from app.models.performance_review import PerformanceReview
from app.models.user import User
from app.schemas.search import (
    EmployeeSearchResponse,
    DepartmentSearchResponse,
    AttendanceSearchResponse,
    LeaveSearchResponse,
    PayrollSearchResponse,
    PerformanceReviewSearchResponse,
)


router = APIRouter(
    prefix="/search",
    tags=["Advanced Search & Filtering"],
)


@router.get(
    "/employees",
    response_model=list[EmployeeSearchResponse],
)
def search_employees(
    q: str | None = Query(
        default=None,
        description="Search by name, email, employee code or designation",
    ),
    department_id: int | None = None,
    status: str | None = None,
    designation: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Employee)

    if q:
        search = f"%{q.strip()}%"

        query = query.filter(
            (
                Employee.first_name.ilike(search)
                | Employee.last_name.ilike(search)
                | Employee.email.ilike(search)
                | Employee.employee_code.ilike(search)
                | Employee.designation.ilike(search)
            )
        )

    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    if status:
        query = query.filter(
            Employee.status == status.upper()
        )

    if designation:
        query = query.filter(
            Employee.designation.ilike(
                f"%{designation.strip()}%"
            )
        )

    return (
        query
        .order_by(Employee.id.desc())
        .all()
    )


@router.get(
    "/departments",
    response_model=list[DepartmentSearchResponse],
)
def search_departments(
    q: str | None = Query(
        default=None,
        description="Search department by name",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Department)

    if q:
        search = f"%{q.strip()}%"

        query = query.filter(
            Department.name.ilike(search)
        )

    return (
        query
        .order_by(Department.name.asc())
        .all()
    )


@router.get(
    "/attendance",
    response_model=list[AttendanceSearchResponse],
)
def search_attendance(
    employee_id: int | None = None,
    status: str | None = None,
    attendance_date: date | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Attendance)

    if employee_id is not None:
        query = query.filter(
            Attendance.employee_id == employee_id
        )

    if status:
        query = query.filter(
            Attendance.status == status.upper()
        )

    if attendance_date:
        query = query.filter(
            Attendance.attendance_date
            == attendance_date
        )

    if start_date:
        query = query.filter(
            Attendance.attendance_date
            >= start_date
        )

    if end_date:
        query = query.filter(
            Attendance.attendance_date
            <= end_date
        )

    return (
        query
        .order_by(
            Attendance.attendance_date.desc()
        )
        .all()
    )


@router.get(
    "/leaves",
    response_model=list[LeaveSearchResponse],
)
def search_leaves(
    employee_id: int | None = None,
    leave_type_id: int | None = None,
    status: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(LeaveRequest)

    if employee_id is not None:
        query = query.filter(
            LeaveRequest.employee_id
            == employee_id
        )

    if leave_type_id is not None:
        query = query.filter(
            LeaveRequest.leave_type_id
            == leave_type_id
        )

    if status:
        query = query.filter(
            LeaveRequest.status
            == status.upper()
        )

    if start_date:
        query = query.filter(
            LeaveRequest.start_date
            >= start_date
        )

    if end_date:
        query = query.filter(
            LeaveRequest.end_date
            <= end_date
        )

    return (
        query
        .order_by(
            LeaveRequest.start_date.desc()
        )
        .all()
    )


@router.get(
    "/payroll",
    response_model=list[PayrollSearchResponse],
)
def search_payroll(
    employee_id: int | None = None,
    pay_period: str | None = None,
    status: str | None = None,
    min_salary: float | None = None,
    max_salary: float | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Payroll)

    if employee_id is not None:
        query = query.filter(
            Payroll.employee_id == employee_id
        )

    if pay_period:
        query = query.filter(
            Payroll.pay_period.ilike(
                f"%{pay_period.strip()}%"
            )
        )

    if status:
        query = query.filter(
            Payroll.status == status.upper()
        )

    if min_salary is not None:
        query = query.filter(
            Payroll.net_salary >= min_salary
        )

    if max_salary is not None:
        query = query.filter(
            Payroll.net_salary <= max_salary
        )

    return (
        query
        .order_by(Payroll.pay_date.desc())
        .all()
    )


@router.get(
    "/performance-reviews",
    response_model=list[
        PerformanceReviewSearchResponse
    ],
)
def search_performance_reviews(
    employee_id: int | None = None,
    review_period: str | None = None,
    status: str | None = None,
    min_rating: float | None = Query(
        default=None,
        ge=1,
        le=5,
    ),
    max_rating: float | None = Query(
        default=None,
        ge=1,
        le=5,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(PerformanceReview)

    if employee_id is not None:
        query = query.filter(
            PerformanceReview.employee_id
            == employee_id
        )

    if review_period:
        query = query.filter(
            PerformanceReview.review_period.ilike(
                f"%{review_period.strip()}%"
            )
        )

    if status:
        query = query.filter(
            PerformanceReview.status
            == status.upper()
        )

    if min_rating is not None:
        query = query.filter(
            PerformanceReview.rating
            >= min_rating
        )

    if max_rating is not None:
        query = query.filter(
            PerformanceReview.rating
            <= max_rating
        )

    return (
        query
        .order_by(
            PerformanceReview.created_at.desc()
        )
        .all()
    )