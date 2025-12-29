from fastapi import APIRouter, Request, Depends
from typing import Dict

from app.auth import get_current_user
from app.config import config
from app.proxy import forward_request

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_product_service(
    path: str,
    request: Request,
    user: Dict = Depends(get_current_user)
):
    """
    Proxy all requests to the Product Service
    Requires authentication
    """
    target_url = f"{config.PRODUCT_SERVICE_URL}/products/{path}"
    return await forward_request(request, target_url, user)


@product_router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def proxy_product_service_root(
    request: Request,
    user: Dict = Depends(get_current_user)
):
    """
    Proxy requests to the Product Service root endpoint
    Requires authentication
    """
    target_url = f"{config.PRODUCT_SERVICE_URL}/products"
    return await forward_request(request, target_url, user)
