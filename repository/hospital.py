from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schemas, models


def get_all(db: Session):
    hospitals = db.query(models.Hospital).all()
    return hospitals


def create(request: schemas.HospitalCreate, db: Session):
    hospital = (
        db.query(models.Hospital).filter(models.Hospital.name == request.name).first()
    )

    if hospital:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Hospital already exists"
        )

    new_hospital = models.Hospital(
        name=request.name,
        address=request.address,
        contact=request.contact,
        email=request.email,
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return new_hospital


def update(request: schemas.Hospital, db: Session):
    hospital = (
        db.query(models.Hospital).filter(models.Hospital.id == request.id).first()
    )
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found"
        )
    hospital.name = request.name
    hospital.address = request.address
    hospital.contact = request.contact
    hospital.email = request.email
    db.commit()
    db.refresh(hospital)
    return hospital


def show(id: int, db: Session):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == id).first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found"
        )
    return hospital


def delete(id: int, db: Session):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == id).first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found"
        )
    db.delete(hospital)
    db.commit()
    return "Hospital deleted successfully"
