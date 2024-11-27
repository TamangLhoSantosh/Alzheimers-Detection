from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# from repository
import database, oauth2

# Initialize the APIRouter for test image-related endpoints with a dynamic hospital and patient ID
router = APIRouter(
    prefix="/hospital/{hospital_id}/patient/{patient_id}/test",  # URL prefix for endpoints
    tags=["Test"],  # Tag for organizing related endpoints
)

# Dependency to get the database session
get_db = database.get_db


# Endpoint to create a test
# - Uses POST method and returns HTTP 201 (created) status code upon success
# Return the created test
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def createTest():
    return {"message": "Test created successfully"}


# Endpoint to fetch all test for a specific patient
# - Uses GET method and returns a list of test images
@router.get("/")
def show_tests():
    return {"message": "Test fetched successfully"}


# Endpoint to fetch a specific test image by ID
# - Uses GET method and returns the details of the specified test image
@router.get("/{id}")
def show_test():
    return {"message": "Test fetched successfully"}
