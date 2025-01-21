from fastapi import (
    APIRouter,
    Depends,
    Query,
    BackgroundTasks,
)
from sqlalchemy.orm import Session
from repository import password_rest

import database, schemas

# Initialize the APIRouter for password reset-related endpoints
# Set the prefix and tags for the router
router = APIRouter(prefix="/password-reset", tags=["Password Reset"])

# Dependency to get the database session
get_db = database.get_db


# Endpoint to request a password reset
# - Uses POST method to send mail to the user's email
# Return success message
@router.post("/request")
async def password_reset_request(
    request: schemas.PasswordResetRequest,  # Request body that must match the `PasswordResetRequest` schema
    bg_task: BackgroundTasks,  # Background tasks to send mail
    db: Session = Depends(get_db),  # Database session dependency injected here
):
    return await password_rest.password_reset_request(request, bg_task, db)


# Endpoint to confirm a password reset
# - Uses POST method to reset password
# Return success message
@router.post("/confirm")
async def password_reset_confirm(
    password: schemas.PasswordResetConfirm,  # Request body that must match the `PasswordResetConfirm` schema
    db: Session = Depends(get_db),  # Database session dependency injected
    token: str = Query(
        ...
    ),  # Token from the query parameters to verify the password reset request
):
    return await password_rest.password_reset_confirm(token, password, db)
