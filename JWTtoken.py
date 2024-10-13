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

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(
    data: dict, expires_delta: timedelta = None, refresh: bool = False
):
    payload = {}
    payload["sub"] = data.get("sub")
    payload["exp"] = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(
    token: str,
    db: Session = Depends(database.get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)

        # Query the database using the provided session (db)
        user = (
            db.query(models.User).filter(models.User.email == token_data.email).first()
        )

        if user is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return user


def verify_user_email(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = schemas.TokenData(email=email)

        user = (
            db.query(models.User).filter(models.User.email == token_data.email).first()
        )
        print(user)
        if user is None:
            raise credentials_exception

        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user.is_verified = True
        db.commit()
        db.refresh(user)

    except JWTError:
        raise credentials_exception

    return "Your email is verified."


def refresh_token(refresh_token: str, db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        # Create a new access token
        new_access_token = create_access_token(data={"sub": user.email})
        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
