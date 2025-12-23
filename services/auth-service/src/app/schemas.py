import enum
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)


class LoginResponse(BaseModel):
    id: str
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
    department_id: int = Field(...)


class RegisterResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    created_at: datetime
    last_login: datetime

    model_config = {
        "from_attributes": True
    }

class RefreshTokenRequest(BaseModel):
    pass


class RefreshTokenResponse(BaseModel):
    pass
