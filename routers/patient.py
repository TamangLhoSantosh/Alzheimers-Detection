from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from repository import patient
import schemas, database, oauth2

router = APIRouter(prefix="/hospital/{hospital_id}/patient", tags=["Patients"])
get_db = database.get_db


@router.get("/", response_model=List[schemas.Patient])
def get_patients(
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(oauth2.get_current_user),
):
    return patient.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_patient(
    request: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(oauth2.get_current_user),
):
    return patient.create(request, db)


@router.get("/{id}", response_model=schemas.Patient)
def get_patient(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(oauth2.get_current_user),
):
    return patient.show(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_patient(
    id: int,
    request: schemas.Patient,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(oauth2.get_current_user),
):
    return patient.update(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(oauth2.get_current_user),
):
    return patient.delete(id, db)
