from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_name: str
    quantity: int = Field(gt=0)


class OrderCreateRequest(BaseModel):
    description: str | None = None
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_name: str
    quantity: int

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    department_id: UUID
    status: str
    description: str | None
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = {"from_attributes": True}
