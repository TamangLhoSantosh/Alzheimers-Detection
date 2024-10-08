from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    first_name: str
    middle_name: str
    last_name: str
    dob: datetime
    gender: str
    contact: str
    address: str
    email: str


class UserCreate(UserBase):
    is_admin: bool
    is_hospital_admin: bool
    password: str
    hospital_id: Optional[int] = None


class UserShow(UserBase):
    id: int
    is_admin: bool
    is_hospital_admin: bool
    hospital_id: Optional[int] = None
    is_verified: bool

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class HospitalBase(BaseModel):
    name: str
    address: str
    contact: str
    email: Optional[str] = None


class HospitalCreate(HospitalBase):
    pass


class Hospital(HospitalBase):
    id: int
    created_at: datetime
    users: Optional[List[UserShow]] = []

    class Config:
        from_attributes = True


class PatientBase(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    dob: datetime
    gender: str
    contact: str
    address: str


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TestImageBase(BaseModel):
    image_url: str
    patient_id: int


class TestImageCreate(TestImageBase):
    pass


class TestImage(TestImageBase):
    id: int

    class Config:
        from_attributes = True


class ResultImageBase(BaseModel):
    image_url: str
    test_image_id: int


class ResultImageCreate(ResultImageBase):
    pass


class ResultImage(ResultImageBase):
    id: int

    class Config:
        from_attributes = True
