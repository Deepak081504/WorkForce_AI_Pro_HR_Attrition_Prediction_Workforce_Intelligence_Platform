from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.shift import Shift
from app.models.user import User
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceUpdate,
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance Management"],
)


@router.post(
    "",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_attendance(
    data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    if data.shift_id is not None:
        shift = (
            db.query(Shift)
            .filter(Shift.id == data.shift_id)
            .first()
        )

        if not shift:
            raise HTTPException(
                status_code=404,
                detail="Shift not found",
            )

    existing = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == data.employee_id,
            Attendance.attendance_date
            == data.attendance_date,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already exists for this employee on this date",
        )

    attendance = Attendance(
        employee_id=data.employee_id,
        shift_id=data.shift_id,
        attendance_date=data.attendance_date,
        check_in=data.check_in,
        check_out=data.check_out,
        status=data.status.upper(),
        remarks=data.remarks,
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


@router.get(
    "",
    response_model=list[AttendanceResponse],
)
def list_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Attendance)
        .order_by(
            Attendance.attendance_date.desc(),
            Attendance.id.desc(),
        )
        .all()
    )


@router.get(
    "/employee/{employee_id}",
    response_model=list[AttendanceResponse],
)
def employee_attendance(
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
        db.query(Attendance)
        .filter(
            Attendance.employee_id == employee_id
        )
        .order_by(
            Attendance.attendance_date.desc()
        )
        .all()
    )


@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attendance = (
        db.query(Attendance)
        .filter(Attendance.id == attendance_id)
        .first()
    )

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found",
        )

    return attendance


@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def update_attendance(
    attendance_id: int,
    data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    attendance = (
        db.query(Attendance)
        .filter(Attendance.id == attendance_id)
        .first()
    )

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found",
        )

    if data.shift_id is not None:
        shift = (
            db.query(Shift)
            .filter(Shift.id == data.shift_id)
            .first()
        )

        if not shift:
            raise HTTPException(
                status_code=404,
                detail="Shift not found",
            )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "status" in update_data:
        update_data["status"] = (
            update_data["status"].upper()
        )

    for field, value in update_data.items():
        setattr(attendance, field, value)

    db.commit()
    db.refresh(attendance)

    return attendance


@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    attendance = (
        db.query(Attendance)
        .filter(Attendance.id == attendance_id)
        .first()
    )

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found",
        )

    db.delete(attendance)
    db.commit()

    return {
        "message": "Attendance deleted successfully"
    }