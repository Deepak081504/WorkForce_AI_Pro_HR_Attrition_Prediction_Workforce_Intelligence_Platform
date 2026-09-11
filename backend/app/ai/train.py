"""
Random Forest training module for employee attrition.
"""

from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier

from app.ai.preprocessing import (
    load_dataset,
    prepare_training_data,
)
from app.ai.feature_engineering import (
    ATTRITION_FEATURES,
)


DEFAULT_MODEL_DIR = Path("ml_models")
DEFAULT_MODEL_PATH = (
    DEFAULT_MODEL_DIR / "attrition_model.joblib"
)


def train_attrition_model(
    dataset_path: str,
    model_path: str | None = None,
) -> dict:
    """
    Train Random Forest attrition model
    and save it as a Joblib file.
    """
    df = load_dataset(dataset_path)

    X, y = prepare_training_data(df)

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    model.fit(X, y)

    output_path = Path(
        model_path
        if model_path
        else DEFAULT_MODEL_PATH
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        output_path,
    )

    return {
        "message": "Attrition model trained successfully",
        "model_path": str(output_path),
        "records_used": len(X),
        "features": ATTRITION_FEATURES,
        "model": "RandomForestClassifier",
        "model_version": "random_forest_v1",
    }


if __name__ == "__main__":
    print(
        "Use train_attrition_model() "
        "from the application or API."
    )