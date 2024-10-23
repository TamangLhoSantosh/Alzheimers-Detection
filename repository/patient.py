from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schemas, models


# Retrieve all patients from the database
def get_all(db: Session):
    patients = db.query(models.Patient).all()
    return patients


# Add patient to the database
def create(
    hospital_id: int,
    current_user: schemas.UserShow,
    request: schemas.PatientCreate,
    db: Session,
):
    # Create a new patient record
    new_patient = models.Patient(
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name,
        dob=request.dob,
        gender=request.gender,
        contact=request.contact,
        address=request.address,
        hospital_id=hospital_id,
        user_id=current_user.id,
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


# To update existing patient
def update(id: int, request: schemas.Patient, db: Session):
    # Retrieve the existing patient record
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    # Update patient details
    patient.first_name = request.first_name
    patient.middle_name = request.middle_name
    patient.last_name = request.last_name
    patient.dob = request.dob
    patient.gender = request.gender
    patient.contact = request.contact
    patient.address = request.address
    db.commit()
    db.refresh(patient)
    return patient

    # Retrieve a specific patient by ID


def show(id: int, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return patient


# To delete specific patient
def delete(id: int, db: Session):
    # Retrieve the patient record to be deleted
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted successfully"}
