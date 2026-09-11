"""
Employee attrition prediction module.
"""

from pathlib import Path

import joblib
import pandas as pd

from app.ai.feature_engineering import (
    ATTRITION_FEATURES,
)
from app.ai.preprocessing import (
    prepare_prediction_data,
)


DEFAULT_MODEL_PATH = Path(
    "ml_models/attrition_model.joblib"
)


def get_risk_level(
    probability: float,
) -> str:
    """
    Convert attrition probability into risk level.
    """
    if probability >= 0.70:
        return "HIGH"

    if probability >= 0.40:
        return "MEDIUM"

    return "LOW"


def load_model(
    model_path: str | None = None,
):
    """
    Load trained Random Forest model.
    """
    path = Path(
        model_path
        if model_path
        else DEFAULT_MODEL_PATH
    )

    if not path.exists():
        raise FileNotFoundError(
            "Attrition model is not trained yet."
        )

    return joblib.load(path)


def predict_attrition(
    employee_data: dict,
    model_path: str | None = None,
) -> dict:
    """
    Predict attrition probability for an employee.
    """
    model = load_model(model_path)

    input_data = prepare_prediction_data(
        employee_data
    )

    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    probability = round(
        probability,
        4,
    )

    risk_level = get_risk_level(
        probability
    )

    return {
        "attrition_probability": probability,
        "risk_level": risk_level,
        "model_version": "random_forest_v1",
        "features_used": ATTRITION_FEATURES,
    }


def predict_from_dataframe(
    df: pd.DataFrame,
    model_path: str | None = None,
) -> pd.DataFrame:
    """
    Generate predictions for multiple employees.
    """
    model = load_model(model_path)

    missing = [
        feature
        for feature in ATTRITION_FEATURES
        if feature not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing columns: "
            + ", ".join(missing)
        )

    X = df[ATTRITION_FEATURES].copy()

    probabilities = model.predict_proba(
        X
    )[:, 1]

    result = df.copy()

    result["attrition_probability"] = (
        probabilities.round(4)
    )

    result["risk_level"] = [
        get_risk_level(
            float(probability)
        )
        for probability in probabilities
    ]

    return result