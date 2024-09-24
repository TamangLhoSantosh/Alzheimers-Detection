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
    gender = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_hospital_admin = Column(Boolean, default=False)
    created_at = Column(Date, nullable=False, default=text("now()"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)

    hospital = relationship("Hospital", back_populates="users")


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("now()"))

    users = relationship("User", back_populates="hospital")
