from typing import Optional
from pydantic import BaseModel


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
    password: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
