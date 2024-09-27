from typing import List
from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm import Session
from repository import user
import schemas, database, oauth2


router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserCreate,
)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=schemas.UserBase)
def show_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(oauth2.get_current_user),
):
    print(current_user)
    return user.show(db, id)
