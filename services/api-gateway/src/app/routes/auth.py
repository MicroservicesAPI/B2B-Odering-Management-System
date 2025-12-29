from fastapi import APIRouter, Request, Depends
from typing import Dict, Optional

from app.auth import get_optional_user
from app.config import config
from app.proxy import forward_request

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_auth_service(
    path: str,
    request: Request,
    user: Optional[Dict] = Depends(get_optional_user)
):
    """
    Proxy all requests to the Auth Service
    Authentication is optional for auth endpoints (login, register)
    """
    target_url = f"{config.AUTH_SERVICE_URL}/auth/{path}"
    return await forward_request(request, target_url, user)
