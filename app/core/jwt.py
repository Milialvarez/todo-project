from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings
from typing import Optional

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    subject: suele ser el id del usuario o el email (string)
    """
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub": str(subject), "exp": expire, "iat": now}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def create_refresh_token(subject: str, expires_delta: timedelta) -> str:
    now = datetime.utcnow()
    expire = now + expires_delta

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": now,
        "type": "refresh"
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
