from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(
    db: Session,
    employee_data: EmployeeCreate,
) -> Employee:

    existing_code = (
        db.query(Employee)
        .filter(Employee.employee_code == employee_data.employee_code)
        .first()
    )

    if existing_code:
        raise ValueError("Employee code already exists")

    existing_email = (
        db.query(Employee)
        .filter(Employee.email == employee_data.email)
        .first()
    )

    if existing_email:
        raise ValueError("Employee email already exists")

    employee = Employee(
        employee_code=employee_data.employee_code,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=employee_data.email,
        phone=employee_data.phone,
        date_of_birth=employee_data.date_of_birth,
        joining_date=employee_data.joining_date,
        designation=employee_data.designation,
        department_id=employee_data.department_id,
        manager_id=employee_data.manager_id,
        status=employee_data.status.upper(),
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def get_employee(
    db: Session,
    employee_id: int,
) -> Employee | None:

    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Employee]:

    return (
        db.query(Employee)
        .order_by(Employee.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee:

    employee = get_employee(db, employee_id)

    if not employee:
        raise ValueError("Employee not found")

    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:
        existing_email = (
            db.query(Employee)
            .filter(
                Employee.email == update_data["email"],
                Employee.id != employee_id,
            )
            .first()
        )

        if existing_email:
            raise ValueError("Employee email already exists")

    for field, value in update_data.items():

        if field == "status" and value:
            value = value.upper()

        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(
    db: Session,
    employee_id: int,
) -> None:

    employee = get_employee(db, employee_id)

    if not employee:
        raise ValueError("Employee not found")

    db.delete(employee)
    db.commit()