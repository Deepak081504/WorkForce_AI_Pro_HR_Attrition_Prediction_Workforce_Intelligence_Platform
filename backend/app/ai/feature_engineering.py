"""
Feature engineering utilities for employee attrition prediction.
"""

import pandas as pd


ATTRITION_FEATURES = [
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

TARGET_COLUMN = "attrition"


def get_feature_columns() -> list[str]:
    """
    Return the feature columns used by the attrition model.
    """
    return ATTRITION_FEATURES.copy()


def validate_features(df: pd.DataFrame) -> list[str]:
    """
    Return missing required columns from a dataframe.
    """
    required = ATTRITION_FEATURES + [TARGET_COLUMN]

    return [
        column
        for column in required
        if column not in df.columns
    ]


def create_feature_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the model input dataframe using required features.
    """
    missing = [
        column
        for column in ATTRITION_FEATURES
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing feature columns: {', '.join(missing)}"
        )

    return df[ATTRITION_FEATURES].copy()


def convert_target(df: pd.DataFrame) -> pd.Series:
    """
    Convert attrition values into binary values.

    YES / 1 -> 1
    NO / 0  -> 0
    """
    if TARGET_COLUMN not in df.columns:
        raise ValueError("Missing attrition column")

    target = (
        df[TARGET_COLUMN]
        .astype(str)
        .str.strip()
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

    return target