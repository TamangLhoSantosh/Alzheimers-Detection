from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas


def create(request: schemas.UserBase, db: Session):
    new_user = models.User(
        username=request.username,
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name,
        gender=request.gender,
        contact=request.contact,
        address=request.address,
        email=request.email,
        password=request.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} is not available"
        )
    return user
