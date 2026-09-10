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
from app.models.performance_review import (
    PerformanceReview,
)
from app.models.user import User
from app.schemas.performance_review import (
    PerformanceReviewCreate,
    PerformanceReviewResponse,
    PerformanceReviewUpdate,
)


router = APIRouter(
    prefix="/performance-reviews",
    tags=["Performance Review System"],
)


@router.post(
    "",
    response_model=PerformanceReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    data: PerformanceReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
            "MANAGER",
        )
    ),
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.id == data.employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    review = PerformanceReview(
        employee_id=data.employee_id,
        reviewer_id=current_user.id,
        review_period=data.review_period,
        rating=data.rating,
        strengths=data.strengths,
        areas_for_improvement=(
            data.areas_for_improvement
        ),
        goals=data.goals,
        feedback=data.feedback,
        status="DRAFT",
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


@router.get(
    "",
    response_model=list[PerformanceReviewResponse],
)
def list_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    if current_user.role in {
        "ADMIN",
        "HR",
        "MANAGER",
    }:
        return (
            db.query(PerformanceReview)
            .order_by(
                PerformanceReview.created_at.desc()
            )
            .all()
        )

    employee = (
        db.query(Employee)
        .filter(
            Employee.email
            == current_user.email
        )
        .first()
    )

    if not employee:
        return []

    return (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.employee_id
            == employee.id
        )
        .order_by(
            PerformanceReview.created_at.desc()
        )
        .all()
    )


@router.get(
    "/employee/{employee_id}",
    response_model=list[PerformanceReviewResponse],
)
def employee_reviews(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.id == employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    if current_user.role == "EMPLOYEE":
        if employee.email != current_user.email:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    return (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.employee_id
            == employee_id
        )
        .order_by(
            PerformanceReview.created_at.desc()
        )
        .all()
    )


@router.get(
    "/{review_id}",
    response_model=PerformanceReviewResponse,
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    review = (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.id == review_id
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found",
        )

    if current_user.role == "EMPLOYEE":
        employee = (
            db.query(Employee)
            .filter(
                Employee.id
                == review.employee_id
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
                detail="Access denied",
            )

    return review


@router.put(
    "/{review_id}",
    response_model=PerformanceReviewResponse,
)
def update_review(
    review_id: int,
    data: PerformanceReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
            "MANAGER",
        )
    ),
):
    review = (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.id == review_id
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "status" in update_data:
        update_data["status"] = (
            update_data["status"].upper()
        )

    for field, value in update_data.items():
        setattr(
            review,
            field,
            value,
        )

    db.commit()
    db.refresh(review)

    return review


@router.patch(
    "/{review_id}/submit",
    response_model=PerformanceReviewResponse,
)
def submit_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
            "MANAGER",
        )
    ),
):
    review = (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.id == review_id
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found",
        )

    if review.status == "COMPLETED":
        raise HTTPException(
            status_code=400,
            detail="Review is already completed",
        )

    review.status = "SUBMITTED"

    db.commit()
    db.refresh(review)

    return review


@router.patch(
    "/{review_id}/complete",
    response_model=PerformanceReviewResponse,
)
def complete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
            "MANAGER",
        )
    ),
):
    review = (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.id == review_id
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found",
        )

    if review.status != "SUBMITTED":
        raise HTTPException(
            status_code=400,
            detail=(
                "Only submitted reviews "
                "can be completed"
            ),
        )

    review.status = "COMPLETED"

    db.commit()
    db.refresh(review)

    return review


@router.delete(
    "/{review_id}"
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
        )
    ),
):
    review = (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.id == review_id
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found",
        )

    db.delete(review)
    db.commit()

    return {
        "message": (
            "Performance review deleted successfully"
        )
    }