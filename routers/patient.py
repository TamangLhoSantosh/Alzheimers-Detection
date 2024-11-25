from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from repository import patient
import schemas, database, oauth2

# Initialize the APIRouter for patient-related endpoints with a dynamic hospital ID
# Set the prefix and tags for the router
router = APIRouter(prefix="/hospital/{hospital_id}/patient", tags=["Patients"])

# Dependency to get the database session
get_db = database.get_db


# Endpoint to retrieve all patients for a specific hospital
# - Uses GET method and returns a list of patients
@router.get(
    "/", response_model=List[schemas.Patient]
)  # Response model specifies the structure of returned data
def get_patients(
    hospital_id: int,  # Hospital ID from the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return patient.get_all_hospital(hospital_id, db)


# Endpoint to create a new patient
# - Uses POST method and returns HTTP 201 (created) status code upon success
# Return the created patient
@router.post(
    "/", status_code=status.HTTP_201_CREATED
)  # Set the status code to 201 Created for successful creation
def create_patient(
    hospital_id: int,  # Hospital ID from the URL path
    request: schemas.PatientCreate,  # Request body that must match the `PatientCreate` schema
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return patient.create(hospital_id, current_user, request, db)


# Endpoint to fetch a specific patient by ID
# - Uses GET method and returns the details of the specified patient
@router.get(
    "/{id}", response_model=schemas.Patient
)  # Path parameter `{id}` to specify the patient ID
def get_patient(
    hospital_id: int,  # Hospital ID from the URL path
    id: int,  # Patient ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return patient.show(id, db)


# Endpoint to update a specific patient by ID
# - Uses PUT method and returns HTTP 202 (accepted) status code upon success
# Return the updated patient information
@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED
)  # Set the status code to 202 Accepted for successful updates
def update_patient(
    hospital_id: int,  # Hospital ID from the URL path
    id: int,  # Patient ID passed in the URL path
    request: schemas.Patient,  # Request body that must match the `Patient` schema
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return patient.update(id, request, db)


# Endpoint to delete a specific patient by ID
# - Uses DELETE method and returns HTTP 204 (no content) status code upon success
# Return confirmation of deletion
@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT
)  # Set the status code to 204 No Content for successful deletions
def delete_patient(
    hospital_id: int,  # Hospital ID from the URL path
    id: int,  # Patient ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return patient.delete(id, db)


# Create a new router for all patients across all hospitals
router_all_patients = APIRouter(prefix="/patient", tags=["Patients"])


# Endpoint to retrieve all patients across all hospitals
@router_all_patients.get("/", response_model=List[schemas.Patient])
def get_all_patients(
    db: Session = Depends(get_db),
    # current_user: schemas.UserBase = Depends(oauth2.get_admin_user),
):
    return patient.get_all(db)
