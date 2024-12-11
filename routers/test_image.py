from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm import Session

from repository import test_image
import schemas, database, oauth2

# Initialize the APIRouter for test image-related endpoints with a dynamic hospital and patient ID
router = APIRouter(
    prefix="/hospital/{hospital_id}/patient/{patient_id}/test/{test_id}/test_image",  # URL prefix for endpoints
    tags=["Test Images"],  # Tag for organizing related endpoints
)

# Dependency to get the database session
get_db = database.get_db


# Endpoint to upload a test image
# - Uses POST method and returns HTTP 201 (created) status code upon success
# Return the created image
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def upload_test_image(
    hospital_id: int,  # Hospital ID from the URL path
    test_id: int,  # Test ID from the URL path
    patient_id: int,  # Patient ID from the URL path
    image: UploadFile,  # Uploaded image file
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserShow = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return await test_image.create(db, image, test_id, patient_id)


# Endpoint to fetch all test images for a specific patient
# - Uses GET method and returns a list of test images
@router.get(
    "/", response_model=list[schemas.TestImage]
)  # Response model specifies the structure of returned data
def show_test_images(
    hospital_id: int,  # Hospital ID from the URL path
    test_id: int,  # Test ID from the URL path
    patient_id: int,  # Patient ID from the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserShow = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return test_image.get_test_images(db, patient_id)


# Endpoint to fetch a specific test image by ID
# - Uses GET method and returns the details of the specified test image
@router.get(
    "/{id}", response_model=schemas.TestImage
)  # Path parameter `{id}` to specify the test image ID
def show_test_image(
    hospital_id: int,  # Hospital ID from the URL path
    test_id,  # Test ID from the URL path
    patient_id: int,  # Patient ID from the URL path
    id: int,  # Test image ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserShow = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return test_image.show(db, id)
