from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from repository import user
import schemas, database


router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserBase,
)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=schemas.UserBase)
def show_user(id: int, db: Session = Depends(get_db)):
    return user.show(db, id)
