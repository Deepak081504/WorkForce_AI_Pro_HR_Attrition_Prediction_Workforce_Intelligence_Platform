from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.employee import Employee
from app.models.payroll import Payroll
from app.models.user import User
from app.schemas.payroll import (
    PayrollCreate,
    PayrollResponse,
    PayrollUpdate,
)

router = APIRouter(
    prefix="/payroll",
    tags=["Payroll Management"],
)


def calculate_salary(
    basic_salary: float,
    allowances: float,
    deductions: float,
    bonus: float,
):
    gross_salary = (
        basic_salary
        + allowances
        + bonus
    )

    net_salary = (
        gross_salary
        - deductions
    )

    return gross_salary, net_salary


@router.post(
    "",
    response_model=PayrollResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payroll(
    data: PayrollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == data.employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    existing = (
        db.query(Payroll)
        .filter(
            Payroll.employee_id == data.employee_id,
            Payroll.pay_period == data.pay_period,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Payroll already exists for this employee and pay period",
        )

    gross_salary, net_salary = calculate_salary(
        basic_salary=data.basic_salary,
        allowances=data.allowances,
        deductions=data.deductions,
        bonus=data.bonus,
    )

    payroll = Payroll(
        employee_id=data.employee_id,
        pay_period=data.pay_period,
        pay_date=data.pay_date,
        basic_salary=data.basic_salary,
        allowances=data.allowances,
        deductions=data.deductions,
        bonus=data.bonus,
        gross_salary=gross_salary,
        net_salary=net_salary,
        status=data.status.upper(),
    )

    db.add(payroll)
    db.commit()
    db.refresh(payroll)

    return payroll


@router.get(
    "",
    response_model=list[PayrollResponse],
)
def list_payroll(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Payroll)
        .order_by(Payroll.id.desc())
        .all()
    )


@router.get(
    "/employee/{employee_id}",
    response_model=list[PayrollResponse],
)
def employee_payroll(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return (
        db.query(Payroll)
        .filter(
            Payroll.employee_id == employee_id
        )
        .order_by(Payroll.pay_date.desc())
        .all()
    )


@router.get(
    "/{payroll_id}",
    response_model=PayrollResponse,
)
def get_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payroll = (
        db.query(Payroll)
        .filter(Payroll.id == payroll_id)
        .first()
    )

    if not payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found",
        )

    return payroll


@router.put(
    "/{payroll_id}",
    response_model=PayrollResponse,
)
def update_payroll(
    payroll_id: int,
    data: PayrollUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    payroll = (
        db.query(Payroll)
        .filter(Payroll.id == payroll_id)
        .first()
    )

    if not payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        if field == "status" and value:
            value = value.upper()

        setattr(payroll, field, value)

    gross_salary, net_salary = calculate_salary(
        basic_salary=payroll.basic_salary,
        allowances=payroll.allowances,
        deductions=payroll.deductions,
        bonus=payroll.bonus,
    )

    payroll.gross_salary = gross_salary
    payroll.net_salary = net_salary

    db.commit()
    db.refresh(payroll)

    return payroll


@router.patch(
    "/{payroll_id}/status",
    response_model=PayrollResponse,
)
def update_payroll_status(
    payroll_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    payroll = (
        db.query(Payroll)
        .filter(Payroll.id == payroll_id)
        .first()
    )

    if not payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found",
        )

    allowed_statuses = {
        "PENDING",
        "PROCESSED",
        "PAID",
        "CANCELLED",
    }

    new_status = status_value.upper()

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid payroll status",
        )

    payroll.status = new_status

    db.commit()
    db.refresh(payroll)

    return payroll


@router.delete("/{payroll_id}")
def delete_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    payroll = (
        db.query(Payroll)
        .filter(Payroll.id == payroll_id)
        .first()
    )

    if not payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found",
        )

    db.delete(payroll)
    db.commit()

    return {
        "message": "Payroll deleted successfully"
    }