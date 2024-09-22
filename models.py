from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(100))
    contact = Column(String(100))
    address = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
