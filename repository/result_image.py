from fastapi import UploadFile
from sqlalchemy.orm import Session
import models
from save_image import save

# Location to store image
DIRNAME = "media/images/result_images"


# Add image url to the database
async def create(db: Session, image: UploadFile, test_image_id: int):
    # Save the uploaded image to the specified directory
    image_path = await save(image, DIRNAME)

    # Create a new ResultImage record
    new_result_image = models.ResultImage(
        image_url=image_path,
        test_image_id=test_image_id,
    )

    # Add and commit the new record to the database
    db.add(new_result_image)
    db.commit()
    db.refresh(new_result_image)
    return new_result_image


# Retrieve result images for a specific test image by ID
def get_result_images(db: Session, test_image_id: int):
    result_images = (
        db.query(models.ResultImage)
        .filter(models.ResultImage.test_image_id == test_image_id)  # Corrected filter
        .all()  # Change to .all() to retrieve all images for the test image
    )
    return result_images
