from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):

    username: str
    first_name: str
    middle_name: str
    last_name: str
    gender: str
    contact: str
    address: str
    email: EmailStr
    password: str
