from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.message import Message
from app.models.user import User
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
)
from app.services.chat_service import (
    get_conversation,
    mark_messages_as_read,
    send_message,
)

router = APIRouter(
    prefix="/chat",
    tags=["One-to-One Chat"],
)


@router.post(
    "/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.receiver_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot send a message to yourself",
        )

    receiver = (
        db.query(User)
        .filter(User.id == data.receiver_id)
        .first()
    )

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found",
        )

    if not receiver.is_active:
        raise HTTPException(
            status_code=400,
            detail="Receiver account is inactive",
        )

    return send_message(
        db=db,
        sender_id=current_user.id,
        receiver_id=data.receiver_id,
        content=data.content,
    )


@router.get(
    "/conversation/{user_id}",
    response_model=list[MessageResponse],
)
def conversation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Invalid conversation user",
        )

    other_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not other_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return get_conversation(
        db=db,
        user_id=current_user.id,
        other_user_id=user_id,
    )


@router.patch(
    "/conversation/{user_id}/read"
)
def mark_conversation_read(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sender = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not sender:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    count = mark_messages_as_read(
        db=db,
        user_id=current_user.id,
        sender_id=user_id,
    )

    return {
        "message": "Messages marked as read",
        "updated_count": count,
    }


@router.get(
    "/unread",
    response_model=list[MessageResponse],
)
def unread_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Message)
        .filter(
            Message.receiver_id == current_user.id,
            Message.is_read == False,
        )
        .order_by(Message.created_at.asc())
        .all()
    )


@router.delete("/messages/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.sender_id == current_user.id,
        )
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    db.delete(message)
    db.commit()

    return {
        "message": "Message deleted successfully"
    }