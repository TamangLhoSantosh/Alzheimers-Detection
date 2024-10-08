import os
from datetime import datetime, timedelta, timezone
from typing import Optional

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


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(
    token: str,
    credentials_exception: HTTPException,
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
        print(payload)
        email: str = payload.get("sub")
        print(email)

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

    return
