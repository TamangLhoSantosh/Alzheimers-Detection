from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm import Session
from repository import result_image
import schemas, database, oauth2


router = APIRouter(
    prefix="/hospital/{hospital_id}/patient/{patient_id}/test/{test_image_id}/result_image",
    tags=["Result Images"],
)
get_db = database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def upload_result_image(
    hospital_id: int,
    patient_id: int,
    test_image_id: int,
    image: UploadFile,
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(oauth2.get_current_user),
):
    return await result_image.create(db, image, test_image_id)


@router.get("/{id}", response_model=schemas.ResultImage)
def show_result_image(
    hospital_id: int,
    patient_id: int,
    test_image_id: int,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserShow = Depends(oauth2.get_current_user),
):
    return result_image.get_result_images(db, id)
