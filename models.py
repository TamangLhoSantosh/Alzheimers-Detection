from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_hospital_admin = Column(Boolean, default=False)
    created_at = Column(Date, nullable=False, default=text("now()"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    is_verified = Column(Boolean, default=False)

    hospital = relationship("Hospital", back_populates="users")
    patients = relationship("Patient", back_populates="user")


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("now()"))

    users = relationship("User", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    created_at = Column(Date, nullable=False, default=text("now()"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    hospital = relationship("Hospital", back_populates="patients")
    user = relationship("User", back_populates="patients")
    test_images = relationship("TestImage", back_populates="patient")


class TestImage(Base):
    __tablename__ = "test_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(2048), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    patient = relationship("Patient", back_populates="test_images")
    result_images = relationship("ResultImage", back_populates="test_image")


class ResultImage(Base):
    __tablename__ = "result_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(2048), nullable=False)
    test_image_id = Column(Integer, ForeignKey("test_images.id"), nullable=False)

    test_image = relationship("TestImage", back_populates="result_images")
