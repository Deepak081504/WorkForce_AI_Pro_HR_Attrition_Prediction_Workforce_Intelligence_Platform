import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy.orm import Session

from app.models.attrition_prediction import AttritionPrediction
from app.schemas.prediction import (
    AttritionPredictionRequest,
)
from app.services.risk_service import update_employee_risk
from app.services.alert_service import (
    create_risk_alerts,
)

MODEL_DIR = "ml_models"
MODEL_PATH = os.path.join(
    MODEL_DIR,
    "attrition_model.joblib",
)


FEATURES = [
    "age",
    "monthly_income",
    "years_at_company",
    "years_in_current_role",
    "job_satisfaction",
    "environment_satisfaction",
    "work_life_balance",
    "overtime",
    "job_level",
    "num_companies_worked",
]


def get_risk_level(
    probability: float,
) -> str:

    if probability >= 0.70:
        return "HIGH"

    if probability >= 0.40:
        return "MEDIUM"

    return "LOW"


def train_model(
    dataset_path: str,
) -> dict:

    if not os.path.exists(dataset_path):
        raise ValueError(
            "Dataset file not found"
        )

    if dataset_path.lower().endswith(".csv"):
        df = pd.read_csv(dataset_path)

    elif dataset_path.lower().endswith(
        (".xlsx", ".xls")
    ):
        df = pd.read_excel(dataset_path)

    else:
        raise ValueError(
            "Unsupported dataset format"
        )

    required_columns = FEATURES + [
        "attrition"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    df = df.dropna(
        subset=required_columns
    )

    if df.empty:
        raise ValueError(
            "Dataset contains no valid records"
        )

    X = df[FEATURES]

    y = (
        df["attrition"]
        .astype(str)
        .str.upper()
        .map(
            {
                "YES": 1,
                "NO": 0,
                "1": 1,
                "0": 0,
            }
        )
    )

    valid_rows = y.notna()

    X = X.loc[valid_rows]
    y = y.loc[valid_rows]

    if y.nunique() < 2:
        raise ValueError(
            "Attrition column must contain both YES and NO values"
        )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X, y)

    os.makedirs(
        MODEL_DIR,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    return {
        "message": "Attrition model trained successfully",
        "model_path": MODEL_PATH,
        "records_used": len(X),
        "features": FEATURES,
    }


def predict_attrition(
    db: Session,
    data: AttritionPredictionRequest,
) -> AttritionPrediction:

    if not os.path.exists(MODEL_PATH):
        raise ValueError(
            "Attrition model is not trained yet"
        )

    model = joblib.load(
        MODEL_PATH
    )

    input_data = pd.DataFrame(
        [
            {
                feature: getattr(
                    data,
                    feature,
                )
                for feature in FEATURES
            }
        ]
    )

    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    risk_level = get_risk_level(
        probability
    )

    prediction = AttritionPrediction(
        employee_id=data.employee_id,
        attrition_probability=round(
            probability,
            4,
        ),
        risk_level=risk_level,
        model_version="random_forest_v1",
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    from app.services.risk_service import (
            update_employee_risk,
    )

    update_employee_risk(
           db=db,
           prediction=prediction,
    )

    create_risk_alerts(
           db=db,
           employee_id=prediction.employee_id,
    )

    return prediction