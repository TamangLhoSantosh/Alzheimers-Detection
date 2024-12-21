from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship
from database import Base


# User model representing system users.
# It contains personal details, contact information, role flags, and relationships to hospitals and patients.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    contact = Column(String(10), nullable=False)
    address = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_hospital_admin = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    is_verified = Column(Boolean, default=False)

    hospital = relationship("Hospital", back_populates="users")
    patients = relationship("Patient", back_populates="user")


# Hospital model representing medical institutions.
# It includes hospital details and relationships to users and patients.
class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    contact = Column(String(10), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    users = relationship("User", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")


# Patient model representing individuals receiving medical care.
# Includes personal details, hospital association, and test images.
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    contact = Column(String(10), nullable=False)
    address = Column(String(100), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    hospital = relationship("Hospital", back_populates="patients")
    user = relationship("User", back_populates="patients")
    tests = relationship("Test", back_populates="patient")
    test_images = relationship("TestImage", back_populates="patient")


# Test model representing medical tests assigned to a patient.
# It contains test description and the result (nullable), along with the relationship to the patient.
class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100), nullable=True)
    result = Column(String(100), nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    patient = relationship("Patient", back_populates="tests")
    test_images = relationship("TestImage", back_populates="test")


# TestImage model representing medical images uploaded for testing.
# These images are analyzed for diagnostic purposes.
class TestImage(Base):
    __tablename__ = "test_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(2048), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    test = relationship("Test", back_populates="test_images")
    patient = relationship("Patient", back_populates="test_images")
