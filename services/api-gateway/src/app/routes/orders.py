from fastapi import APIRouter, Request, Depends
from typing import Dict

from app.auth import get_current_user
from app.config import config
from app.proxy import forward_request

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_order_service(
    path: str,
    request: Request,
    user: Dict = Depends(get_current_user)
):
    """
    Proxy all requests to the Order Service
    Requires authentication
    """
    target_url = f"{config.ORDER_SERVICE_URL}/orders/{path}"
    return await forward_request(request, target_url, user)


@order_router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def proxy_order_service_root(
    request: Request,
    user: Dict = Depends(get_current_user)
):
    """
    Proxy requests to the Order Service root endpoint
    Requires authentication
    """
    target_url = f"{config.ORDER_SERVICE_URL}/orders"
    return await forward_request(request, target_url, user)
