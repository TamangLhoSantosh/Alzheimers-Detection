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

# Retrieve JWT configuration settings from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Default expiration time for access tokens


def raise_credentials_exception(
    status: str = status.HTTP_401_UNAUTHORIZED,
    detail: str = "Could not validate credentials",
):
    """Raise an HTTPException for invalid credentials."""
    raise HTTPException(
        status_code=status,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def decode_token(token: str) -> dict:
    """Decode the JWT token and return the payload.

    Raises an exception if the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise_credentials_exception(detail="Token is invalid")


def get_user_from_email(email: str, db: Session) -> models.User:
    """Fetch a user from the database using their email.

    Raises an exception if the user is not found.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise_credentials_exception("User Not Found")
    return user


def create_access_token(
    data: dict, expires_delta: timedelta = None, refresh: bool = False
) -> str:
    """Create an access token with the specified claims and expiration time."""
    expire = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Define the payload for the JWT
    payload = {
        "sub": data.get("sub"),
        "is_admin": data.get("is_admin"),
        "is_hospital_admin": data.get("is_hospital_admin"),
        "hospital_id": data.get("hospital_id"),
        "exp": datetime.now(timezone.utc) + expire,
        "jti": str(uuid.uuid4()),
        "iat": datetime.now(timezone.utc),
        "refresh": refresh,
    }

    # Encode the payload into a JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_user_email(token: str, db: Session):
    """Verify a user's email using the provided token.

    Updates the user's verification status in the database.
    """
    payload = decode_token(token)

    email: str = payload.get("sub")
    if email is None:
        raise_credentials_exception()

    token_data = schemas.TokenData(email=email)

    user = get_user_from_email(token_data.email, db)

    # Check if the user is already verified
    if user.is_verified:
        raise_credentials_exception(status.HTTP_409_CONFLICT, "Email already verified")

    user.is_verified = True
    db.commit()
    db.refresh(user)

    return "Your email is verified."


def verify_access_token(
    token: str, db: Session = Depends(database.get_db)
) -> models.User:
    """Verify the access token and return the associated user."""
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
    """Verify the refresh token and return a new access token."""
    payload = decode_token(refresh_token)
    if not payload.get("refresh"):
        raise_credentials_exception(detail="Invalid refresh token")

    email: str = payload.get("sub")
    if email is None:
        raise_credentials_exception()

    user = get_user_from_email(email, db)

    new_access_token = create_access_token(
        data={
            "sub": user.email,
            "is_admin": user.is_admin,
            "is_hospital_admin": user.is_hospital_admin,
            "hospital_id": user.hospital_id,
        }
    )

    # Return the new access token
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }
