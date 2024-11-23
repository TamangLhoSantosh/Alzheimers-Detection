from typing import Optional
from fastapi import APIRouter, Depends, status, BackgroundTasks, Query
from sqlalchemy.orm import Session

from repository import user
import schemas, database, oauth2


# Initialize the APIRouter for user-related endpoints with the prefix `/user`
router = APIRouter(prefix="/user", tags=["Users"])

# Dependency to get the database session
get_db = database.get_db


# Endpoint to create a new user
# - Uses POST method and returns HTTP 201 (created) status code upon success
# - Response model: `schemas.UserCreate` - to ensure consistent response structure
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserCreate,
)
async def create_user(
    request: schemas.UserCreate,  # Request body that must match the `UserCreate` schema
    bg_task: BackgroundTasks,  # Background tasks to send email verification mail
    db: Session = Depends(get_db),  # Database session dependency
):
    return await user.create(request, bg_task, db)


# Endpoint to fetch a user by ID
# - Uses GET method and returns the user data based on the `UserBase` schema
@router.get("/{id}", response_model=schemas.UserBase)
def show_user(
    id: int,  # The user ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return user.show(db, id)


# Endpoint to fetch all users
# - Uses GET method and returns a list of users based on the `UserShow` schema
@router.get("/", response_model=list[schemas.UserShow])
def list_users(
    hospital_id: Optional[int] = Query(
        None
    ),  # Optional query parameter to filter users by hospital ID
    db: Session = Depends(get_db),  # Database session dependency
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    print("method")
    return user.get_all(hospital_id, db)


# Endpoint to update user by ID
# - Uses PUT method and returns HTTP 202 (accepted) status code upon success
# - Request model: `schemas.UserShow` - to ensure the request body structure
@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserShow
)
def update_user(
    id: int,  # The user ID passed in the URL path
    request: schemas.UserShow,  # Request body that must match the `UserShow` schema
    db: Session = Depends(get_db),  # Database session dependency
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return user.update(db, id, request)


# Endpoint to delete user by ID
# - Uses DELETE method and returns HTTP 204 (no content) status code upon success
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,  # The user ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return user.delete(db, id)
