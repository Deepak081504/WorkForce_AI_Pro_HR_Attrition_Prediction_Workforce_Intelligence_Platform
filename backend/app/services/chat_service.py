from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.message import Message


def send_message(
    db: Session,
    sender_id: int,
    receiver_id: int,
    content: str,
) -> Message:

    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        is_read=False,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation(
    db: Session,
    user_id: int,
    other_user_id: int,
) -> list[Message]:

    return (
        db.query(Message)
        .filter(
            or_(
                (
                    (Message.sender_id == user_id)
                    & (Message.receiver_id == other_user_id)
                ),
                (
                    (Message.sender_id == other_user_id)
                    & (Message.receiver_id == user_id)
                ),
            )
        )
        .order_by(Message.created_at.asc())
        .all()
    )


def mark_messages_as_read(
    db: Session,
    user_id: int,
    sender_id: int,
) -> int:

    messages = (
        db.query(Message)
        .filter(
            Message.sender_id == sender_id,
            Message.receiver_id == user_id,
            Message.is_read == False,
        )
        .all()
    )

    for message in messages:
        message.is_read = True

    db.commit()

    return len(messages)