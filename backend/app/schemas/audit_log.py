from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    resource_type: str
    resource_id: int | None
    description: str | None
    ip_address: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )