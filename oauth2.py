from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import JWTtoken, schemas, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    data: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
):

    return JWTtoken.verify_token(data, db)


def get_admin_user(
    current_user: schemas.UserShow = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough clearance to access this resource",
        )
    return current_user
