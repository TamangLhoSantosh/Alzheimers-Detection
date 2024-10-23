from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import JWTtoken, schemas, database

# OAuth2PasswordBearer is a FastAPI dependency that retrieves the token from the request.
# This will be used to extract the token from the Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    data: str = Depends(
        oauth2_scheme
    ),  # Dependency that retrieves the token from the request
    db: Session = Depends(
        database.get_db
    ),  # Dependency that provides a database session
):
    """Verify the access token and return the current user."""
    return JWTtoken.verify_access_token(data, db)


def get_admin_user(
    current_user: schemas.UserShow = Depends(
        get_current_user
    ),  # Dependency that gets the current user
):
    """Check if the current user is an admin; raises an exception if not."""
    if not current_user.is_admin:  # Check if the user is an admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Raise a 403 Forbidden error if not an admin
            detail="You do not have enough clearance to access this resource",
        )

    # Return the current user if they are an admin
    return current_user
