from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Query,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from hashing import Hash
import JWTtoken, database, models, schemas

# Initialize the APIRouter for authentication-related endpoints
# Set the tags for the router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Define an HTTP exception for unauthorized access due to invalid credentials
credentials_exception = HTTPException(
    # Set the status code to 401 Unauthorized
    status_code=status.HTTP_401_UNAUTHORIZED,
    # Detail message for the exception
    detail="Could not validate credentials",
    # Specify the authentication method in the headers
    headers={"WWW-Authenticate": "Bearer"},
)


# Endpoint for user login
@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),  # Automatically parse the login form request
    db: Session = Depends(database.get_db),  # Database session dependency injected here
):
    # Query the database to find the user by email (username)
    user = db.query(models.User).filter(models.User.email == request.username).first()

    # Check if the user exists
    if not user:
        raise HTTPException(
            # Set the status code to 400 Unauthorized
            status_code=status.HTTP_400_BAD_REQUEST,
            # Detail message for the exception
            detail="Invalid Credentials",
        )  # Raise an exception if user not found

    # Verify the provided password against the hashed password in the database
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            # Set the status code to 400 Unauthorized
            status_code=status.HTTP_400_BAD_REQUEST,
            # Detail message for the exception
            detail="Invalid Credentials",
        )  # Raise an exception if password verification fails

    # Generate an access token with user details
    access_token = JWTtoken.create_access_token(
        data={
            "sub": user.email,
            "is_admin": user.is_admin,
            "is_hospital_admin": user.is_hospital_admin,
            "hospital_id": user.hospital_id,
        }
    )

    # Generate a refresh token with an expiration time of 7 days
    refresh_token = JWTtoken.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=7),
        refresh=True,
    )

    # User's full name to send
    userName = user.first_name + user.middle_name + user.last_name

    # Return a JSON response with the tokens and user information
    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "is_admin": user.is_admin,
            "is_hospital_admin": user.is_hospital_admin,
            "user": userName,
            "hospital_id": user.hospital_id,
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK,
    )


# Endpoint to verify user email via a token
@router.get("/verify-email/")
def verify_user_account(
    token: str = Query(...),  # Expects a token as a query parameter
    db: Session = Depends(database.get_db),  # Database session dependency injected here
):
    # Call the JWT token verification function to verify the user account
    return JWTtoken.verify_user_email(token, db)


# Endpoint to refresh an access token
@router.post("/refresh-token")
def refresh_token(
    refresh_token: schemas.TokenRefreshRequest,  # Expect a refresh token in the request body
    db: Session = Depends(database.get_db),  # Database session dependency injected here
):
    # Call the function to verify the refresh token and generate a new access token
    return JWTtoken.verify_refresh_token(refresh_token, db)
