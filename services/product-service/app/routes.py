from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.db import get_db
from app.schemas import ProductResponse, ProductCreate, ProductUpdate, StockAdjustment
from app.service import ProductService

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.post("", response_model=ProductResponse)
def create_product(
    request: ProductCreate,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    """Create a new product (Admin only)"""
    try:
        return ProductService.create_product(db, request, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@product_router.get("/list", response_model=list[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    """List all products"""
    return ProductService.list_products(db, user, skip=skip, limit=limit)


@product_router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    """Get product details by ID"""
    try:
        return ProductService.get_product(db, product_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@product_router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    request: ProductUpdate,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    """Update product details (Admin only)"""
    try:
        return ProductService.update_product(db, product_id, request, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@product_router.patch("/{product_id}/stock", response_model=ProductResponse)
def adjust_stock(
    product_id: str,
    request: StockAdjustment,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    """Adjust stock level (Admin only)"""
    try:
        return ProductService.adjust_stock(db, product_id, request, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
