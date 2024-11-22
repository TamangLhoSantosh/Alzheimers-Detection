import datetime
from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import models, schemas, hashing, JWTtoken
from email_utils import send_verification_email


# Retrieve all users from the database
def get_all(db: Session):
    users = db.query(models.User).all()
    return users


# Add user to the database
async def create(request: schemas.UserCreate, bg_task: BackgroundTasks, db: Session):
    # Check if the hospital exists if hospital_id is provided
    if request.hospital_id is not None:
        hospital = (
            db.query(models.Hospital)
            .filter(models.Hospital.id == request.hospital_id)
            .first()
        )
        if not hospital:
            raise HTTPException(status_code=400, detail="Hospital not found")

    # Check if a user with the given email already exists
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {request.email} already exists",
        )

    # Check if a user with the given username already exists
    user = (
        db.query(models.User).filter(models.User.username == request.username).first()
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username {request.username} already exists",
        )

    # Create new user instance
    new_user = models.User(
        username=request.username,
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name,
        dob=request.dob,
        gender=request.gender,
        contact=request.contact,
        address=request.address,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password),  # Hash the password
        is_admin=request.is_admin,
        is_hospital_admin=request.is_hospital_admin,
        hospital_id=request.hospital_id,
    )
    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create a JWT token for email verification
    expires_delta = datetime.timedelta(hours=24)
    verification_token = JWTtoken.create_access_token(
        data={"sub": new_user.email}, expires_delta=expires_delta
    )

    # Send verification email in the background
    bg_task.add_task(send_verification_email, new_user.email, verification_token)

    return new_user


# Retrieve a user by ID
def show(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not available",
        )
    return user
