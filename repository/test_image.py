from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import models
from save_image import save
from image_analysis import analyze_image

# Location to store image
DIRNAME = "media/images/test_images"


# Add image url to the database
async def create(db: Session, image: UploadFile, test_id: int, patient_id: int):
    # Save the uploaded image to the specified directory
    image_path = await save(image, DIRNAME)

    # Create a new TestImage record
    new_test_image = models.TestImage(
        image_url=image_path,
        test_id=test_id,
        patient_id=patient_id,
    )

    # Add and commit the new record to the database
    db.add(new_test_image)
    db.commit()
    db.refresh(new_test_image)

    try:
        # Call the Analysis Service to process the uploaded image
        analysis_response = await analyze_image(image_path)
        print(analysis_response)

        analysis_result = analysis_response.get("prediction")

        if analysis_result is None:
            raise ValueError("No result found in the analysis response.")

        # Fetch the corresponding test from the database
        test = db.query(models.Test).filter(models.Test.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test not found.")

        # Update the test record with the analysis result
        test.result = analysis_result
        db.commit()

        # Return the newly created test image
        return new_test_image

    except Exception as e:
        # If an error occurs, delete the record from the database and rollback the changes
        db.delete(new_test_image)
        db.commit()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {e}",
        )


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
