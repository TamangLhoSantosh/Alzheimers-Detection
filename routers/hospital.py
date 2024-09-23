from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database

router = APIRouter(prefix="/hospital", tags=["Hospitals"])
get_db = database.get_db


@router.get("/", response_model=List[schemas.Hospital])
def get_hospitals(db: Session = Depends(get_db)):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_hospital(request: schemas.Hospital, db: Session = Depends(get_db)):
    pass


@router.get("/{id}", response_model=schemas.Hospital)
def get_hospital(id: int, db: Session = Depends(get_db)):
    pass


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_hospital(id: int, request: schemas.Hospital, db: Session = Depends(get_db)):
    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hospital(id: int, db: Session = Depends(get_db)):
    pass
