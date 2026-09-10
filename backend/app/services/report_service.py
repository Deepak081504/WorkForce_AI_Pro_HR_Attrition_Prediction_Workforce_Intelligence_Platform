import io

import pandas as pd
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.employee_risk import EmployeeRisk
from app.models.leave_request import LeaveRequest
from app.models.payroll import Payroll


def get_employee_report(db: Session):
    records = (
        db.query(Employee)
        .order_by(Employee.id)
        .all()
    )

    return [
        {
            "employee_id": employee.id,
            "employee_code": employee.employee_code,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "designation": employee.designation,
            "department_id": employee.department_id,
            "manager_id": employee.manager_id,
            "joining_date": employee.joining_date,
            "status": employee.status,
        }
        for employee in records
    ]


def get_attendance_report(db: Session):
    records = (
        db.query(Attendance)
        .order_by(
            Attendance.attendance_date.desc()
        )
        .all()
    )

    return [
        {
            "attendance_id": record.id,
            "employee_id": record.employee_id,
            "shift_id": record.shift_id,
            "attendance_date": record.attendance_date,
            "check_in": record.check_in,
            "check_out": record.check_out,
            "status": record.status,
            "remarks": record.remarks,
        }
        for record in records
    ]


def get_leave_report(db: Session):
    records = (
        db.query(LeaveRequest)
        .order_by(
            LeaveRequest.created_at.desc()
        )
        .all()
    )

    return [
        {
            "leave_id": record.id,
            "employee_id": record.employee_id,
            "leave_type_id": record.leave_type_id,
            "start_date": record.start_date,
            "end_date": record.end_date,
            "reason": record.reason,
            "status": record.status,
        }
        for record in records
    ]


def get_payroll_report(db: Session):
    records = (
        db.query(Payroll)
        .order_by(Payroll.pay_date.desc())
        .all()
    )

    return [
        {
            "payroll_id": record.id,
            "employee_id": record.employee_id,
            "pay_period": record.pay_period,
            "pay_date": record.pay_date,
            "basic_salary": record.basic_salary,
            "allowances": record.allowances,
            "deductions": record.deductions,
            "bonus": record.bonus,
            "gross_salary": record.gross_salary,
            "net_salary": record.net_salary,
            "status": record.status,
        }
        for record in records
    ]


def get_attrition_risk_report(db: Session):
    records = (
        db.query(EmployeeRisk)
        .order_by(
            EmployeeRisk.risk_score.desc()
        )
        .all()
    )

    return [
        {
            "risk_id": record.id,
            "employee_id": record.employee_id,
            "risk_score": record.risk_score,
            "risk_level": record.risk_level,
            "risk_reason": record.risk_reason,
            "last_prediction_id": (
                record.last_prediction_id
            ),
            "updated_at": record.updated_at,
        }
        for record in records
    ]


def create_csv(data: list[dict]) -> io.BytesIO:
    dataframe = pd.DataFrame(data)

    output = io.BytesIO()

    dataframe.to_csv(
        output,
        index=False,
    )

    output.seek(0)

    return output


def create_excel(data: list[dict]) -> io.BytesIO:
    dataframe = pd.DataFrame(data)

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Report",
        )

    output.seek(0)

    return output