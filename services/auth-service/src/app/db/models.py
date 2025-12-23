import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Enum,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base
from app.schemas import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.STAFF
    )

    department_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    last_login = Column(DateTime, nullable=True)


class Department(Base):
    __tablename__ = "departments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
