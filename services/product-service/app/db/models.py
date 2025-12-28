import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db import Base


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


class Product(Base):
    __tablename__ = "products"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
