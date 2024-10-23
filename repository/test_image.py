from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import models
from save_image import save

# Location to store image
DIRNAME = "media/images/result_images"


# Add image url to the database
async def create(db: Session, image: UploadFile, patient_id: int):
    # Save the uploaded image to the specified directory
    image_path = await save(image, DIRNAME)

    # Create a new TestImage record
    new_test_image = models.TestImage(
        image_url=image_path,
        patient_id=patient_id,
    )

    # Add and commit the new record to the database
    db.add(new_test_image)
    db.commit()
    db.refresh(new_test_image)
    return new_test_image


def show(db: Session, id: int):
    # Retrieve a specific test image by ID
    test_image = db.query(models.TestImage).filter(models.TestImage.id == id).first()
    if not test_image:
        raise HTTPException(
            status_code=404, detail=f"Test Image with id {id} not found"
        )
    return test_image


# Retrieve all test images for a specific patient
def get_test_images(db: Session, patient_id: int):
    test_images = (
        db.query(models.TestImage)
        .filter(models.TestImage.patient_id == patient_id)
        .all()
    )
    return test_images
