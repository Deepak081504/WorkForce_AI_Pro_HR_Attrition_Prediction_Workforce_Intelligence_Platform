from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    employee_id: int
    uploaded_by: int
    document_name: str
    document_type: str
    file_path: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )