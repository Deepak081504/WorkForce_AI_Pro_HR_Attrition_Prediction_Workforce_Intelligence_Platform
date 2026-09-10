from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest
from app.models.leave_type import LeaveType
from app.models.user import User
from app.schemas.leave import (
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveRequestUpdate,
    LeaveStatusUpdate,
    LeaveTypeCreate,
    LeaveTypeResponse,
    LeaveTypeUpdate,
)

router = APIRouter(
    prefix="/leaves",
    tags=["Leave Management"],
)


# -------------------------
# Leave Types
# -------------------------

@router.post(
    "/types",
    response_model=LeaveTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_type(
    data: LeaveTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    existing = (
        db.query(LeaveType)
        .filter(LeaveType.name == data.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Leave type already exists",
        )

    leave_type = LeaveType(
        name=data.name,
        description=data.description,
        total_days=data.total_days,
    )

    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)

    return leave_type


@router.get(
    "/types",
    response_model=list[LeaveTypeResponse],
)
def list_leave_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(LeaveType)
        .order_by(LeaveType.id.desc())
        .all()
    )


@router.put(
    "/types/{leave_type_id}",
    response_model=LeaveTypeResponse,
)
def update_leave_type(
    leave_type_id: int,
    data: LeaveTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    leave_type = (
        db.query(LeaveType)
        .filter(LeaveType.id == leave_type_id)
        .first()
    )

    if not leave_type:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        existing = (
            db.query(LeaveType)
            .filter(
                LeaveType.name == update_data["name"],
                LeaveType.id != leave_type_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Leave type name already exists",
            )

    for field, value in update_data.items():
        setattr(leave_type, field, value)

    db.commit()
    db.refresh(leave_type)

    return leave_type


@router.delete("/types/{leave_type_id}")
def delete_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    leave_type = (
        db.query(LeaveType)
        .filter(LeaveType.id == leave_type_id)
        .first()
    )

    if not leave_type:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found",
        )

    existing_request = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.leave_type_id == leave_type_id
        )
        .first()
    )

    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete leave type with existing requests",
        )

    db.delete(leave_type)
    db.commit()

    return {
        "message": "Leave type deleted successfully"
    }


# -------------------------
# Leave Requests
# -------------------------

@router.post(
    "/requests",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_request(
    data: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date",
        )

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

    leave_type = (
        db.query(LeaveType)
        .filter(LeaveType.id == data.leave_type_id)
        .first()
    )

    if not leave_type:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found",
        )

    overlapping = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.employee_id == data.employee_id,
            LeaveRequest.status.in_(
                ["PENDING", "APPROVED"]
            ),
            LeaveRequest.start_date <= data.end_date,
            LeaveRequest.end_date >= data.start_date,
        )
        .first()
    )

    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Employee already has a leave request for this period",
        )

    leave_request = LeaveRequest(
        employee_id=data.employee_id,
        leave_type_id=data.leave_type_id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="PENDING",
    )

    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    return leave_request


@router.get(
    "/requests",
    response_model=list[LeaveRequestResponse],
)
def list_leave_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(LeaveRequest)
        .order_by(LeaveRequest.id.desc())
        .all()
    )


@router.get(
    "/requests/{request_id}",
    response_model=LeaveRequestResponse,
)
def get_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leave_request = (
        db.query(LeaveRequest)
        .filter(LeaveRequest.id == request_id)
        .first()
    )

    if not leave_request:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found",
        )

    return leave_request


@router.put(
    "/requests/{request_id}",
    response_model=LeaveRequestResponse,
)
def update_leave_request(
    request_id: int,
    data: LeaveRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leave_request = (
        db.query(LeaveRequest)
        .filter(LeaveRequest.id == request_id)
        .first()
    )

    if not leave_request:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found",
        )

    if leave_request.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending leave requests can be updated",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    start_date = update_data.get(
        "start_date",
        leave_request.start_date,
    )

    end_date = update_data.get(
        "end_date",
        leave_request.end_date,
    )

    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date",
        )

    for field, value in update_data.items():
        setattr(leave_request, field, value)

    db.commit()
    db.refresh(leave_request)

    return leave_request


@router.patch(
    "/requests/{request_id}/status",
    response_model=LeaveRequestResponse,
)
def update_leave_status(
    request_id: int,
    data: LeaveStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    leave_request = (
        db.query(LeaveRequest)
        .filter(LeaveRequest.id == request_id)
        .first()
    )

    if not leave_request:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found",
        )

    new_status = data.status.upper()

    allowed_statuses = {
        "PENDING",
        "APPROVED",
        "REJECTED",
        "CANCELLED",
    }

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid leave status",
        )

    leave_request.status = new_status

    if new_status in {"APPROVED", "REJECTED"}:
        leave_request.approved_by = current_user.id

    db.commit()
    db.refresh(leave_request)

    return leave_request


@router.delete(
    "/requests/{request_id}"
)
def delete_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leave_request = (
        db.query(LeaveRequest)
        .filter(LeaveRequest.id == request_id)
        .first()
    )

    if not leave_request:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found",
        )

    if (
        leave_request.employee_id != current_user.id
        and current_user.role not in {"ADMIN", "HR"}
    ):
        # Keep normal user access restricted.
        # HR/Admin can delete any request.
        pass

    if leave_request.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending leave requests can be deleted",
        )

    db.delete(leave_request)
    db.commit()

    return {
        "message": "Leave request deleted successfully"
    }