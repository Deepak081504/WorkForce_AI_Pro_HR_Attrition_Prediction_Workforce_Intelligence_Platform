from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    user_id: int

    title: str = Field(
        min_length=2,
        max_length=150,
    )

    message: str = Field(
        min_length=1,
        max_length=1000,
    )

    notification_type: str = Field(
        default="INFO",
        max_length=50,
    )


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )