from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee_service import (
    create_employee,
    delete_employee,
    get_employee,
    get_employees,
    update_employee,
)
from app.services.audit_service import create_audit_log

router = APIRouter(
    prefix="/employees",
    tags=["Employee Management"],
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_endpoint(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    try:
        new_employee = create_employee(
            db=db,
            employee_data=employee_data,
        )

        create_audit_log(
            db=db,
            user_id=current_user.id,
            action="CREATE",
            resource_type="EMPLOYEE",
            resource_id=new_employee.id,
            description=f"Created employee {getattr(new_employee, 'employee_code', new_employee.id)}",
        )

        return new_employee

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[EmployeeResponse],
)
def list_employees(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_employees(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = get_employee(
        db=db,
        employee_id=employee_id,
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee_endpoint(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    try:
        updated_employee = update_employee(
            db=db,
            employee_id=employee_id,
            employee_data=employee_data,
        )

        create_audit_log(
            db=db,
            user_id=current_user.id,
            action="UPDATE",
            resource_type="EMPLOYEE",
            resource_id=updated_employee.id,
            description=f"Updated employee {getattr(updated_employee, 'employee_code', updated_employee.id)}",
        )

        return updated_employee

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{employee_id}",
)
def delete_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    try:
        
        employee = get_employee(db=db, employee_id=employee_id)
        emp_code = getattr(employee, "employee_code", employee_id) if employee else employee_id

        delete_employee(
            db=db,
            employee_id=employee_id,
        )

        create_audit_log(
            db=db,
            user_id=current_user.id,
            action="DELETE",
            resource_type="EMPLOYEE",
            resource_id=employee_id,
            description=f"Deleted employee {emp_code}",
        )

        return {
            "message": "Employee deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )