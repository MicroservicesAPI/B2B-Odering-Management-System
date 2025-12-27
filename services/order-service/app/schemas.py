from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    completed = "completed"
    cancelled = "cancelled"


class OrderItemCreate(BaseModel):
    product_name: str
    quantity: int = Field(gt=0)
    # unit_price: float = Field(gt=0)


class OrderItemResponse(OrderItemCreate):
    id: UUID

    model_config = {"from_attributes": True}


class OrderCreateRequest(BaseModel):
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    department_id: UUID
    status: OrderStatus
    # total_price: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]

    model_config = {"from_attributes": True}
