from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
import schemas, models


# Retrieve all hospitals from the database
def get_all(db: Session):
    hospitals = db.query(models.Hospital).all()
    return hospitals


# Add hospital to the database
def create(request: schemas.HospitalCreate, db: Session):
    # Check if a hospital with the same name or email already exists
    hospital = (
        db.query(models.Hospital)
        .filter(
            or_(
                models.Hospital.name == request.name,
                models.Hospital.email == request.email,
            )
        )
        .first()
    )

    if hospital:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Hospital already exists"
        )

    # Create a new hospital record
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


# To update existing hospital
def update(request: schemas.Hospital, db: Session):
    # Retrieve the existing hospital record
    hospital = (
        db.query(models.Hospital).filter(models.Hospital.id == request.id).first()
    )
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found"
        )
    # Update hospital details
    hospital.name = request.name
    hospital.address = request.address
    hospital.contact = request.contact
    hospital.email = request.email
    hospital.updated_at = request.updated_at
    db.commit()
    db.refresh(hospital)
    return hospital


# Retrieve a specific hospital by ID
def show(id: int, db: Session):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == id).first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found"
        )
    return hospital


# To delete specific hospital
def delete(id: int, db: Session):
    # Retrieve the hospital record to be deleted
    hospital = db.query(models.Hospital).filter(models.Hospital.id == id).first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found"
        )
    db.delete(hospital)
    db.commit()
    return "Hospital deleted successfully"
