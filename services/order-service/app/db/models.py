import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

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


class OrderStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), nullable=False)
    department_id = Column(Integer, nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=False)

    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
