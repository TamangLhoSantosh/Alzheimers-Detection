from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    first_name: str
    middle_name: str
    last_name: str
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
