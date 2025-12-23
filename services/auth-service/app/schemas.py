import enum
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)


class LoginResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: str

    model_config = {
        "from_attributes": True
    }


class UserRole(enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    role: UserRole = Field(default=UserRole.STAFF)
    department_id: uuid.UUID = Field(...)


class RegisterResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    role: str
    created_at: datetime
    last_login: datetime

    model_config = {
        "from_attributes": True
    }


class RefreshTokenRequest(BaseModel):
    """ schema of the refresh token request"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """ schema of the refresh token response"""
    access_token: str
    token_type: str = "bearer"
