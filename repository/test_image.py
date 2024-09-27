from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import schemas, models
from save_image import save


def create(db: Session, image: UploadFile, patient_id: int):
    image_path = save(image, "media/images/test_images")
    new_test_image = models.TestImage(
        image=image_path,
        patient_id=patient_id,
    )
    db.add(new_test_image)
    db.commit()
    db.refresh(new_test_image)
    return new_test_image


def show(db: Session, id: int):
    test_image = db.query(models.TestImage).filter(models.TestImage.id == id).first()
    if not test_image:
        raise HTTPException(
            status_code=404, detail=f"Test Image with id {id} not found"
        )
    return test_image


def get_test_images(db: Session, patient_id: int):
    test_images = (
        db.query(models.TestImage)
        .filter(models.TestImage.patient_id == patient_id)
        .all()
    )
    return test_images
