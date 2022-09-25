from datetime import datetime, timedelta
from typing import Optional

from jwt import decode, encode
from fastapi import HTTPException, status

from settings import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> dict:
    to_jwt_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.JWT_EXPIRES_TIME)

    to_jwt_encode.update({"exp": expire})
    encoded_jwt = encode(to_jwt_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str):
    try:
        data = decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
