from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

# This is the one that was missing!
class UserCreate(UserBase):
    email: str
    password: str
    full_name: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True