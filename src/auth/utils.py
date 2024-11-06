from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
from fastapi import HTTPException, status
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadData
from passlib.context import CryptContext

from src.config import Config

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRY = 3600  # seconds
REFRESH_TOKEN_EXPIRY = 1  # day


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> None:
    if not password_context.verify(password, hash=password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def create_token(
    user_data: dict[str, str],
    refresh: bool = False,
) -> str:
    return jwt.encode(
        payload={
            "user": user_data,
            "exp": datetime.now(UTC)
            + (
                timedelta(days=REFRESH_TOKEN_EXPIRY)
                if refresh
                else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
            ),
            "jti": str(uuid4()),
            "refresh": refresh,
        },
        key=Config.JWT_SECRET,
        algorithm="HS256",
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has Expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt="email-verification"
)


def create_url_safe_token(data: dict[str, Any]) -> str:
    return serializer.dumps(data)


def decode_url_safe_token(token: str) -> dict[str, Any]:
    try:
        return serializer.loads(token)
    except BadData:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
