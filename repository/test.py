from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas


# Create a new test entry for a patient
def create_test(db: Session, request: schemas.TestCreate, patient_id: int):
    # Create a new Test record
    new_test = models.Test(
        description=request.description,
        patient_id=patient_id,
    )

    # Add and commit the new test to the database
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test


# Retrieve all tests for a specific patient
def get_tests(db: Session, patient_id: int):
    # Query all tests for the given patient ID
    tests = db.query(models.Test).filter(models.Test.patient_id == patient_id).all()
    return tests


# Retrieve a specific test by ID
def get_test_by_id(db: Session, test_id: int):
    # Query for a specific test by its ID
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail=f"Test with id {test_id} not found")
    return test


# Update the result of a specific test
def update_test_result(db: Session, test_id: int, result: str):
    # Find the test by its ID
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail=f"Test with id {test_id} not found")

    # Update the result of the test
    test.result = result
    db.commit()
    db.refresh(test)
    return test
