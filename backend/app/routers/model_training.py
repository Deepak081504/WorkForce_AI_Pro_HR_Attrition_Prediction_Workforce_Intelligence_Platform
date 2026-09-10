from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.dataset import Dataset
from app.models.user import User
from app.services.attrition_service import (
    train_model,
)


router = APIRouter(
    prefix="/ml",
    tags=["AI Model Training"],
)


@router.post("/train/{dataset_id}")
def train_attrition_model(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id
        )
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    try:
        return train_model(
            dataset.file_path
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )