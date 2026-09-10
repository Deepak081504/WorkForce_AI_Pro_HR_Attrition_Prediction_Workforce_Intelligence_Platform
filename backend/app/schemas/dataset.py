from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DatasetResponse(BaseModel):
    id: int
    name: str
    description: str | None
    file_name: str
    file_path: str
    file_type: str
    uploaded_by: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )