from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, hashing


def create(request: schemas.UserCreate, db: Session):
    if request.hospital_id is not None:
        hospital = (
            db.query(models.Hospital)
            .filter(models.Hospital.id == request.hospital_id)
            .first()
        )
        if not hospital:
            raise HTTPException(status_code=400, detail="Hospital not found")
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {request.email} already exists",
        )

    user = (
        db.query(models.User).filter(models.User.username == request.username).first()
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username {request.username} already exists",
        )

    new_user = models.User(
        username=request.username,
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name,
        gender=request.gender,
        contact=request.contact,
        address=request.address,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password),
        is_admin=request.is_admin,
        is_hospital_admin=request.is_hospital_admin,
        hospital_id=request.hospital_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not available",
        )
    return user