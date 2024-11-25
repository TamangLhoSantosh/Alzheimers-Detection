from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    """Base model for user-related information."""

    username: str
    first_name: str
    middle_name: str
    last_name: str
    dob: datetime  # Date of birth
    gender: str
    contact: str
    address: str
    email: str
    hospital_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    is_admin: bool  # Indicates if the user is an admin
    is_hospital_admin: bool  # Indicates if the user is a hospital admin


class UserCreate(UserBase):
    """Model for creating a new user, extending UserBase with additional fields."""

    password: str


class UserShow(UserBase):
    """Model for displaying user information, including an ID and verification status."""

    id: int
    is_verified: bool

    class Config:
        from_attributes = True  # Allows the use of attributes from the database


class Login(BaseModel):
    """Model for user login credentials."""

    username: str
    password: str


class Token(BaseModel):
    """Model for the authentication token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for the token payload data."""

    email: Optional[str] = None


class HospitalBase(BaseModel):
    """Base model for hospital-related information."""

    name: str
    address: str
    contact: str
    email: Optional[str] = None


class HospitalCreate(HospitalBase):
    """Model for creating a new hospital, extending HospitalBase."""

    pass


class Hospital(HospitalBase):
    """Model for displaying hospital information, including an ID and associated users."""

    id: int
    updated_at: Optional[datetime] = None
    users: Optional[List[UserShow]] = []

    class Config:
        from_attributes = True  # Allows the use of attributes from the database


class PatientBase(BaseModel):
    """Base model for patient-related information."""

    first_name: str
    middle_name: Optional[str]
    last_name: str
    dob: datetime  # Date of birth
    gender: str
    contact: str
    address: str
    hospital_id: int


class PatientCreate(PatientBase):
    """Model for creating a new patient, extending PatientBase."""

    pass


class Patient(PatientBase):
    """Model for displaying patient information, including an ID and creation timestamp."""

    id: int

    class Config:
        from_attributes = True  # Allows the use of attributes from the database


class TestImageBase(BaseModel):
    """Base model for test image-related information."""

    image_url: str
    patient_id: int


class TestImageCreate(TestImageBase):
    """Model for creating a new test image, extending TestImageBase."""

    pass


class TestImage(TestImageBase):
    """Model for displaying test image information, including an ID."""

    id: int

    class Config:
        from_attributes = True  # Allows the use of attributes from the database


class ResultImageBase(BaseModel):
    """Base model for result image-related information."""

    image_url: str
    test_image_id: int


class ResultImageCreate(ResultImageBase):
    """Model for creating a new result image, extending ResultImageBase."""

    pass


class ResultImage(ResultImageBase):
    """Model for displaying result image information, including an ID."""

    id: int

    class Config:
        from_attributes = True  # Allows the use of attributes from the database


class PasswordReset(BaseModel):
    """Model for initiating a password reset."""

    email: str


class PasswordResetRequest(PasswordReset):
    """Model for requesting a password reset, extending PasswordReset."""

    pass


class PasswordResetConfirm(BaseModel):
    """Model for confirming a password reset with new passwords."""

    new_password: str


class TokenRefreshRequest(BaseModel):
    """Model for refreshing a token."""

    refresh_token: str
