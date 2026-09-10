from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User


ALLOWED_ROLES = {
    "ADMIN",
    "HR",
    "MANAGER",
    "EMPLOYEE"
}


def register_user(
    db: Session,
    full_name: str,
    email: str,
    password: str,
    role: str
) -> User:

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        raise ValueError("Email already registered")

    role = role.upper()

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid role")

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User | None:

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    if not user.is_active:
        return None

    return user


def generate_tokens(user: User) -> dict:

    access_token = create_access_token(
        user_id=user.id,
        role=user.role
    )

    refresh_token = create_refresh_token(
        user_id=user.id,
        role=user.role
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_access_token(
    db: Session,
    refresh_token: str
) -> dict:

    payload = decode_token(refresh_token)

    if not payload:
        raise ValueError("Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")

    user_id = payload.get("sub")

    if not user_id:
        raise ValueError("Invalid refresh token payload")

    try:
        user_id = int(user_id)
    except ValueError:
        raise ValueError("Invalid user ID")

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise ValueError("User not found")

    if not user.is_active:
        raise ValueError("User account is inactive")

    access_token = create_access_token(
        user_id=user.id,
        role=user.role
    )

    new_refresh_token = create_refresh_token(
        user_id=user.id,
        role=user.role
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


def generate_password_reset_token(
    db: Session,
    email: str
) -> str:

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise ValueError("User not found")

    return create_reset_token(email)


def reset_password(
    db: Session,
    token: str,
    new_password: str
) -> User:

    payload = decode_token(token)

    if not payload:
        raise ValueError("Invalid or expired reset token")

    if payload.get("type") != "password_reset":
        raise ValueError("Invalid password reset token")

    email = payload.get("sub")

    if not email:
        raise ValueError("Invalid reset token")

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise ValueError("User not found")

    user.password_hash = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return user