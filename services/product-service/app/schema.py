from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    stock_quantity: int = Field(default=0, ge=0)
    min_stock: int = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    min_stock: int | None = Field(None, ge=0)


class StockAdjustment(BaseModel):
    quantity: int = Field(..., ge=0)


class ProductResponse(BaseModel):
    id: UUID
    name: str
    sku: str
    description: str | None
    stock_quantity: int
    min_stock: int
    created_at: datetime

    model_config = {"from_attributes": True}