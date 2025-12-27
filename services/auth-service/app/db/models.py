import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Enum,
    TypeDecorator,
    CHAR
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db import Base
from app.schemas import UserRole


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    
    Uses PostgreSQL's UUID type for PostgreSQL databases.
    For other databases (like SQLite), uses CHAR(32) to store UUIDs as 32-character hex strings (without hyphens).
    This ensures compatibility across different database backends for testing and production.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value).hex
            else:
                return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            else:
                return value


class User(Base):
    __tablename__ = "users"

    id = Column(
        GUID(),
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
        GUID(),
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
        GUID(),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
