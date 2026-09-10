from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.employee import Employee
from app.models.task import Task
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Workflow & Task Management"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.id == data.assigned_to
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    task = Task(
        title=data.title,
        description=data.description,
        assigned_to=data.assigned_to,
        created_by=current_user.id,
        priority=data.priority.upper(),
        status="TODO",
        due_date=data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get(
    "",
    response_model=list[TaskResponse],
)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    # Admin/HR/Manager can see all tasks.
    if current_user.role in {
        "ADMIN",
        "HR",
        "MANAGER",
    }:
        return (
            db.query(Task)
            .order_by(
                Task.created_at.desc()
            )
            .all()
        )

    # Employee sees only their assigned tasks.
    return (
        db.query(Task)
        .join(
            Employee,
            Task.assigned_to == Employee.id,
        )
        .filter(
            Employee.email == current_user.email
        )
        .order_by(
            Task.created_at.desc()
        )
        .all()
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    if current_user.role == "EMPLOYEE":
        employee = (
            db.query(Employee)
            .filter(
                Employee.id
                == task.assigned_to
            )
            .first()
        )

        if (
            not employee
            or employee.email
            != current_user.email
        ):
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this task",
            )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    # Employees can only update task status.
    if current_user.role == "EMPLOYEE":

        employee = (
            db.query(Employee)
            .filter(
                Employee.id
                == task.assigned_to
            )
            .first()
        )

        if (
            not employee
            or employee.email
            != current_user.email
        ):
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this task",
            )

        allowed = {"status"}

        if not set(update_data).issubset(
            allowed
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Employees can only "
                    "update task status"
                ),
            )

    else:
        if current_user.role not in {
            "ADMIN",
            "HR",
            "MANAGER",
        }:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

    if "priority" in update_data:
        update_data["priority"] = (
            update_data["priority"].upper()
        )

    if "status" in update_data:
        update_data["status"] = (
            update_data["status"].upper()
        )

    if "assigned_to" in update_data:

        employee = (
            db.query(Employee)
            .filter(
                Employee.id
                == update_data["assigned_to"]
            )
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Assigned employee not found",
            )

    for field, value in update_data.items():
        setattr(
            task,
            field,
            value,
        )

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }