"""
Machine Learning model registry utilities.
"""

from datetime import datetime
from pathlib import Path


MODEL_REGISTRY = {
    "attrition": {
        "model_name": "Random Forest Classifier",
        "model_version": "random_forest_v1",
        "file_name": "attrition_model.joblib",
    },
    "workforce_forecasting": {
        "model_name": "Linear Regression",
        "model_version": "linear_regression_v1",
        "file_name": None,
    },
}


def get_model_info(
    model_name: str,
) -> dict:
    """
    Get registered model information.
    """
    if model_name not in MODEL_REGISTRY:
        raise ValueError(
            f"Model '{model_name}' is not registered."
        )

    return MODEL_REGISTRY[model_name].copy()


def list_models() -> list[dict]:
    """
    Return all registered AI models.
    """
    models = []

    for name, config in MODEL_REGISTRY.items():
        models.append(
            {
                "name": name,
                **config,
            }
        )

    return models


def get_model_path(
    model_name: str,
    base_directory: str = "ml_models",
) -> str | None:
    """
    Return model file path for registered model.
    """
    info = get_model_info(model_name)

    file_name = info.get("file_name")

    if not file_name:
        return None

    return str(
        Path(base_directory) / file_name
    )


def create_model_metadata(
    model_name: str,
) -> dict:
    """
    Create metadata for a model execution.
    """
    info = get_model_info(model_name)

    return {
        "model_name": info["model_name"],
        "model_version": info["model_version"],
        "created_at": datetime.utcnow().isoformat(),
    }