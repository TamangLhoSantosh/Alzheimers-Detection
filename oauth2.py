from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import JWTtoken, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return JWTtoken.verify_token(data, credentials_exception)


def get_admin_user(
    current_user=Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    print(current_user.email)
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough clearance to access this resource",
        )
    return user
