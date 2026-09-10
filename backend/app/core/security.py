from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str
) -> str:

    payload = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    payload.update({
        "exp": expire,
        "type": token_type
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_access_token(
    user_id: int,
    role: str
) -> str:

    return create_token(
        data={
            "sub": str(user_id),
            "role": role
        },
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        token_type="access"
    )


def create_refresh_token(
    user_id: int,
    role: str
) -> str:

    return create_token(
        data={
            "sub": str(user_id),
            "role": role
        },
        expires_delta=timedelta(days=7),
        token_type="refresh"
    )


def create_reset_token(email: str) -> str:

    return create_token(
        data={
            "sub": email
        },
        expires_delta=timedelta(minutes=15),
        token_type="password_reset"
    )


def decode_token(token: str) -> Optional[dict]:

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None