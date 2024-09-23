from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from repository import hospital
import schemas, database

router = APIRouter(prefix="/hospital", tags=["Hospitals"])
get_db = database.get_db


@router.get("/", response_model=List[schemas.Hospital])
def get_hospitals(db: Session = Depends(get_db)):
    return hospital.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_hospital(request: schemas.HospitalBase, db: Session = Depends(get_db)):
    return hospital.create(request, db)


@router.get("/{id}", response_model=schemas.Hospital)
def get_hospital(id: int, db: Session = Depends(get_db)):
    return hospital.show(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_hospital(id: int, request: schemas.Hospital, db: Session = Depends(get_db)):
    return hospital.update(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hospital(id: int, db: Session = Depends(get_db)):
    return hospital.delete(id, db)
