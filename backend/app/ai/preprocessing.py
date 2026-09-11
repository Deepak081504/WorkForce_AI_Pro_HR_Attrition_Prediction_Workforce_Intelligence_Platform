"""
Data preprocessing utilities for HR datasets.
"""

from pathlib import Path

import pandas as pd

from app.ai.feature_engineering import (
    ATTRITION_FEATURES,
    TARGET_COLUMN,
    convert_target,
)


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load CSV or Excel HR dataset.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(path)

    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    raise ValueError(
        "Unsupported dataset format. "
        "Use CSV or Excel."
    )


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset and remove invalid records.
    """
    required_columns = ATTRITION_FEATURES + [
        TARGET_COLUMN
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

    cleaned = df.copy()

    cleaned = cleaned.dropna(
        subset=required_columns
    )

    if cleaned.empty:
        raise ValueError(
            "Dataset contains no valid records."
        )

    return cleaned


def prepare_training_data(
    df: pd.DataFrame,
):
    """
    Prepare X and y for machine learning.
    """
    cleaned = clean_dataset(df)

    X = cleaned[ATTRITION_FEATURES].copy()

    y = convert_target(cleaned)

    valid_rows = y.notna()

    X = X.loc[valid_rows]
    y = y.loc[valid_rows].astype(int)

    if X.empty:
        raise ValueError(
            "No valid training records found."
        )

    if y.nunique() < 2:
        raise ValueError(
            "Attrition column must contain both "
            "YES and NO values."
        )

    return X, y


def prepare_prediction_data(
    data: dict,
) -> pd.DataFrame:
    """
    Prepare one employee record for prediction.
    """
    missing = [
        feature
        for feature in ATTRITION_FEATURES
        if feature not in data
    ]

    if missing:
        raise ValueError(
            "Missing prediction features: "
            + ", ".join(missing)
        )

    return pd.DataFrame(
        [
            {
                feature: data[feature]
                for feature in ATTRITION_FEATURES
            }
        ]
    )