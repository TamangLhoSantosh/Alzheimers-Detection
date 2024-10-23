from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from repository import hospital
import schemas, database, oauth2

# Initialize the APIRouter for hospital-related endpoints
# Set the prefix and tags for the router
router = APIRouter(prefix="/hospital", tags=["Hospitals"])

# Dependency to get the database session
get_db = database.get_db


# Endpoint to retrieve all hospitals
# - Uses GET method and returns a list of hospitals
@router.get(
    "/", response_model=List[schemas.Hospital]
)  # Response model specifies the structure of returned data
def get_hospitals(
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_admin_user
    ),  # OAuth2 dependency to verify the current user as admin
):
    return hospital.get_all(db)


# Endpoint to create a new hospital
# - Uses POST method and returns HTTP 201 (created) status code upon success
# Return the created hospital
@router.post(
    "/", status_code=status.HTTP_201_CREATED
)  # Set the status code to 201 Created for successful creation
def create_hospital(
    request: schemas.HospitalCreate,  # Request body that must match the `HospitalCreate` schema
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_admin_user
    ),  # OAuth2 dependency to verify the current user as admin
):
    return hospital.create(request, db)


# Endpoint to fetch a specific hospital by ID
# - Uses GET method and returns the details of the specified hospital
@router.get(
    "/{id}", response_model=schemas.Hospital
)  # Path parameter `{id}` to specify the hospital ID
def get_hospital(
    id: int,  # Hospital ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return hospital.show(id, db)


# Endpoint to update a specific hospital by ID
# - Uses PUT method and returns HTTP 202 (accepted) status code upon success
# Return the updated hospital information
@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED
)  # Set the status code to 202 Accepted for successful updates
def update_hospital(
    id: int,  # Hospital ID passed in the URL path
    request: schemas.Hospital,  # Request body that must match the `Hospital` schema
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_admin_user
    ),  # OAuth2 dependency to verify the current user as admin
):
    return hospital.update(request, db)  # Return the updated hospital information


# Endpoint to delete a specific hospital by ID
# - Uses DELETE method and returns HTTP 204 (no content) status code upon success
# Return confirmation of deletion
@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT
)  # Set the status code to 204 No Content for successful deletions
def delete_hospital(
    id: int,  # Hospital ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_admin_user
    ),  # OAuth2 dependency to verify the current user as admin
):
    return hospital.delete(id, db)
