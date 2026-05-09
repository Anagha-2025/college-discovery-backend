from sqlalchemy import Column, Integer, String, Boolean, Float
from .database import Base

# This was missing or removed!
class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    fees = Column(Integer)
    rating = Column(Float)
    official_website = Column(String, nullable=True)

# This is the one we added for Auth
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)