"""
Machine Learning model evaluation utilities.
"""

from typing import Any

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


def evaluate_model(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    """
    Evaluate a trained classification model.
    """
    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
    )

    report = classification_report(
        y_test,
        predictions,
        zero_division=0,
    )

    return {
        "accuracy": round(
            float(accuracy),
            4,
        ),
        "precision": round(
            float(precision),
            4,
        ),
        "recall": round(
            float(recall),
            4,
        ),
        "f1_score": round(
            float(f1),
            4,
        ),
        "confusion_matrix": matrix.tolist(),
        "classification_report": report,
    }