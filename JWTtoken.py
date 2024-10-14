import os
from datetime import datetime, timedelta, timezone
import uuid

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from dotenv import load_dotenv

import schemas
import database
import models

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def raise_credentials_exception(
    status: str = status.HTTP_401_UNAUTHORIZED,
    detail: str = "Could not validate credentials",
):
    raise HTTPException(
        status_code=status,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise_credentials_exception()


def get_user_from_email(email: str, db: Session) -> models.User:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise_credentials_exception("User Not Found")
    return user


def create_access_token(
    data: dict, expires_delta: timedelta = None, refresh: bool = False
) -> str:
    expire = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": data.get("sub"),
        "exp": datetime.now(timezone.utc) + expires_delta,
        "jti": str(uuid.uuid4()),
        "iat": datetime.now(timezone.utc),
        "refresh": refresh,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_user_email(token: str, db: Session):
    payload = decode_token(token)

    email: str = payload.get("sub")
    if email is None:
        raise_credentials_exception()

    token_data = schemas.TokenData(email=email)

    user = get_user_from_email(token_data.email, db)

    if user.is_verified:
        raise_credentials_exception(status.HTTP_409_CONFLICT, "Email already verified")

    user.is_verified = True
    db.commit()
    db.refresh(user)

    return "Your email is verified."


def verify_access_token(
    token: str, db: Session = Depends(database.get_db)
) -> models.User:
    payload = decode_token(token)
    if payload.get("refresh"):
        raise_credentials_exception(detail="Invalid access token")

    email: str = payload.get("sub")
    if email is None:
        raise_credentials_exception()

    user = get_user_from_email(email, db)

    return user


def verify_refresh_token(
    refresh_token: str, db: Session = Depends(database.get_db)
) -> dict:
    payload = decode_token(refresh_token)
    if not payload.get("refresh"):
        raise_credentials_exception(detail="Invalid refresh token")

    email: str = payload.get("sub")
    if email is None:
        raise_credentials_exception()

    user = get_user_from_email(email, db)

    # Create a new access token
    new_access_token = create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}
