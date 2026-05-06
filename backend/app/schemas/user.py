from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from app.models.user import UserRole

# Shared properties
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    full_name: str
    date_of_birth: date
    address: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.user

# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID
    role: UserRole
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
