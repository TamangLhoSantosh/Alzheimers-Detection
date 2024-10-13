from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from hashing import Hash
import JWTtoken, database, models, schemas

router = APIRouter(tags=["Authentication"])


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise credentials_exception

    if not Hash.verify(user.password, request.password):
        raise credentials_exception

    # generate a JWT token and return
    access_token = JWTtoken.create_access_token(data={"sub": user.email})
    refresh_token = JWTtoken.create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(days=2), refresh=True
    )
    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.email,
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/verify-email/")
def verify_user_account(
    token: str = Query(...),
    db: Session = Depends(database.get_db),
):
    return JWTtoken.verify_user_email(token, db)


@router.post("/refresh-token")
def refresh_token(
    refresh_token: schemas.TokenRefreshRequest, db: Session = Depends(database.get_db)
):
    return JWTtoken.refresh_token(refresh_token, db)
