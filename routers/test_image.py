from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm import Session
from repository import test_image
import schemas, database, oauth2


router = APIRouter(
    prefix="/hospital/{hospital_id}/patient/{patient_id}/test_image",
    tags=["Test Images"],
)
get_db = database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def upload_test_image(
    hospital_id: int,
    patient_id: int,
    image: UploadFile,
    db: Session = Depends(get_db),
):
    return test_image.create(db, image, patient_id)


@router.get("/", response_model=list[schemas.TestImage])
def show_test_images(
    patient_id: int,
    db: Session = Depends(get_db),
):
    return test_image.get_test_images(db, patient_id)


@router.get("/{id}", response_model=schemas.TestImage)
def show_test_image(
    id: int,
    db: Session = Depends(get_db),
):
    return test_image.show(db, id)
