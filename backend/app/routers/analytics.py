from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.attendance import Attendance
from app.models.department import Department
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest
from app.models.payroll import Payroll
from app.models.user import User
from app.schemas.analytics import (
    AttendanceAnalytics,
    DepartmentAnalytics,
    LeaveAnalytics,
    PayrollAnalytics,
    WorkforceSummary,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Dashboard & Workforce Analytics"],
)


@router.get(
    "/summary",
    response_model=WorkforceSummary,
)
def workforce_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_employees = (
        db.query(Employee)
        .count()
    )

    active_employees = (
        db.query(Employee)
        .filter(Employee.status == "ACTIVE")
        .count()
    )

    inactive_employees = (
        db.query(Employee)
        .filter(Employee.status != "ACTIVE")
        .count()
    )

    total_departments = (
        db.query(Department)
        .count()
    )

    today = date.today()

    present_today = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today,
            Attendance.status == "PRESENT",
        )
        .count()
    )

    absent_today = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today,
            Attendance.status == "ABSENT",
        )
        .count()
    )

    on_leave_today = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.start_date <= today,
            LeaveRequest.end_date >= today,
            LeaveRequest.status == "APPROVED",
        )
        .count()
    )

    total_payroll_records = (
        db.query(Payroll)
        .count()
    )

    total_payroll_amount = (
        db.query(
            func.coalesce(
                func.sum(Payroll.net_salary),
                0,
            )
        )
        .scalar()
    )

    pending_leave_requests = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.status == "PENDING"
        )
        .count()
    )

    approved_leave_requests = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.status == "APPROVED"
        )
        .count()
    )

    rejected_leave_requests = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.status == "REJECTED"
        )
        .count()
    )

    return WorkforceSummary(
        total_employees=total_employees,
        active_employees=active_employees,
        inactive_employees=inactive_employees,
        total_departments=total_departments,
        present_today=present_today,
        absent_today=absent_today,
        on_leave_today=on_leave_today,
        total_payroll_records=total_payroll_records,
        total_payroll_amount=float(
            total_payroll_amount or 0
        ),
        pending_leave_requests=pending_leave_requests,
        approved_leave_requests=approved_leave_requests,
        rejected_leave_requests=rejected_leave_requests,
    )


@router.get(
    "/departments",
    response_model=list[DepartmentAnalytics],
)
def department_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            Department.id,
            Department.name,
            func.count(Employee.id),
        )
        .outerjoin(
            Employee,
            Employee.department_id == Department.id,
        )
        .group_by(
            Department.id,
            Department.name,
        )
        .order_by(
            Department.id
        )
        .all()
    )

    return [
        DepartmentAnalytics(
            department_id=row[0],
            department_name=row[1],
            employee_count=row[2],
        )
        for row in results
    ]


@router.get(
    "/attendance",
    response_model=list[AttendanceAnalytics],
)
def attendance_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            Attendance.status,
            func.count(Attendance.id),
        )
        .group_by(Attendance.status)
        .order_by(Attendance.status)
        .all()
    )

    return [
        AttendanceAnalytics(
            status=row[0],
            count=row[1],
        )
        for row in results
    ]


@router.get(
    "/leaves",
    response_model=list[LeaveAnalytics],
)
def leave_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            LeaveRequest.status,
            func.count(LeaveRequest.id),
        )
        .group_by(LeaveRequest.status)
        .order_by(LeaveRequest.status)
        .all()
    )

    return [
        LeaveAnalytics(
            status=row[0],
            count=row[1],
        )
        for row in results
    ]


@router.get(
    "/payroll",
    response_model=list[PayrollAnalytics],
)
def payroll_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            Payroll.pay_period,
            func.count(Payroll.employee_id),
            func.coalesce(
                func.sum(Payroll.gross_salary),
                0,
            ),
            func.coalesce(
                func.sum(Payroll.net_salary),
                0,
            ),
        )
        .group_by(Payroll.pay_period)
        .order_by(Payroll.pay_period.desc())
        .all()
    )

    return [
        PayrollAnalytics(
            pay_period=row[0],
            employee_count=row[1],
            total_gross_salary=float(row[2]),
            total_net_salary=float(row[3]),
        )
        for row in results
    ]