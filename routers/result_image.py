from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm import Session

from repository import result_image
import schemas, database, oauth2

# Initialize the APIRouter for result image-related endpoints with a dynamic hospital, patient, and test image ID
router = APIRouter(
    prefix="/hospital/{hospital_id}/patient/{patient_id}/test/{test_image_id}/result_image",  # URL prefix for endpoints
    tags=["Result Images"],  # Tag for organizing related endpoints
)

# Dependency to get the database session
get_db = database.get_db


# Endpoint to upload a result image
# - Uses POST method and returns HTTP 201 (created) status code upon success
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,  # Set the status code to 201 Created for successful uploads
)
async def upload_result_image(
    hospital_id: int,  # Hospital ID from the URL path
    patient_id: int,  # Patient ID from the URL path
    test_image_id: int,  # Test image ID from the URL path
    image: UploadFile,  # Uploaded image file
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserShow = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return await result_image.create(db, image, test_image_id)


# Endpoint to fetch a specific result image by ID
# - Uses GET method and returns the details of the specified result image
@router.get(
    "/{id}", response_model=schemas.ResultImage
)  # Path parameter `{id}` to specify the result image ID
def show_result_image(
    hospital_id: int,  # Hospital ID from the URL path
    patient_id: int,  # Patient ID from the URL path
    test_image_id: int,  # Test image ID from the URL path
    id: int,  # Result image ID passed in the URL path
    db: Session = Depends(get_db),  # Database session dependency injected here
    current_user: schemas.UserShow = Depends(
        oauth2.get_current_user
    ),  # OAuth2 dependency to verify the current user
):
    return result_image.get_result_images(db, id)
