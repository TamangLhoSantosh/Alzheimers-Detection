from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schemas, models


def get_all(db: Session):
    patients = db.query(models.Patient).all()
    return patients


def create(
    hospital_id: int,
    current_user: schemas.UserShow,
    request: schemas.PatientCreate,
    db: Session,
):
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


def update(request: schemas.Patient, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == request.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    patient.first_name = (request.first_name,)
    patient.middle_name = (request.middle_name,)
    patient.last_name = (request.last_name,)
    patient.dob = (request.dob,)
    patient.gender = (request.gender,)
    patient.contact = (request.contact,)
    patient.address = (request.address,)
    db.commit()
    db.refresh(patient)
    return patient


def show(id: int, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return patient


def delete(id: int, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    db.delete(patient)
    db.commit()
    return "Patient deleted successfully"
