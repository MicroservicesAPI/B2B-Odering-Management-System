from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.db import get_db
from app.db.models import OrderStatus
from app.schemas import OrderResponse, OrderCreateRequest
from app.services import OrderService

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("", response_model=OrderResponse)
def create_order(
    request: OrderCreateRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return OrderService.create_order(db, request, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@order_router.get("", response_model=list[OrderResponse])
def list_orders(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    return OrderService.list_orders(db, user)


@order_router.get("/me", response_model=list[OrderResponse])
def get_my_orders(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    """Get orders for the current user"""
    return OrderService.get_my_orders(db, user)


@order_router.put("/{order_id}/status")
def update_order_status(
    order_id: str,
    status: OrderStatus,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return OrderService.update_order_status(db, order_id, status, user)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
