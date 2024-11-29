from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from repository import test
import database, schemas, oauth2

# Initialize the APIRouter for test-related endpoints
router = APIRouter(
    prefix="/hospital/{hospital_id}/patient/{patient_id}/test",
    tags=["Test"],
)

# Dependency to get the database session
get_db = database.get_db


# Endpoint to create a test
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.TestCreate
)
async def create_test(
    hospital_id: int,
    patient_id: int,
    description: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return test.create_test(db, description, patient_id)


# Endpoint to fetch all tests for a specific patient
@router.get("/", response_model=list[schemas.Test])
def show_tests(
    hospital_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return test.get_tests(db, patient_id)


# Endpoint to fetch a specific test by ID
@router.get("/{id}", response_model=schemas.Test)
def show_test(
    hospital_id: int,
    patient_id: int,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return test.get_test_by_id(db, id)


# Endpoint to update the result of a specific test
@router.put("/{id}/result", response_model=schemas.Test)
def update_test_result(
    hospital_id: int,
    patient_id: int,
    id: int,
    result: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return test.update_test_result(db, id, result)
