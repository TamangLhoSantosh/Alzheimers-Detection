from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import models
from save_image import save

DIRNAME = "media/images/result_images"


async def create(db: Session, image: UploadFile, result_image_id: int):
    image_path = await save(image, DIRNAME)
    new_result_image = models.ResultImage(
        image_url=image_path,
        result_image_id=result_image_id,
    )
    db.add(new_result_image)
    db.commit()
    db.refresh(new_result_image)
    return new_result_image


def get_result_images(db: Session, result_image_id: int):
    result_images = (
        db.query(models.ResultImage)
        .filter(models.ResultImage.id == result_image_id)
        .first()
    )
    return result_images.image_url
