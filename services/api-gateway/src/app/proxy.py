import httpx
from fastapi import HTTPException, Request, Response
from typing import Dict, Optional


async def forward_request(
    request: Request,
    target_url: str,
    user_data: Optional[Dict] = None
) -> Response:
    """
    Forward the incoming request to a target service
    
    Args:
        request: The incoming FastAPI request
        target_url: The target service URL
        user_data: Optional user data from JWT to inject into headers
        
    Returns:
        Response from the target service
    """
    # Get request body if present
    body = await request.body()
    
    # Prepare headers
    headers = dict(request.headers)
    
    # Remove host header to avoid conflicts
    headers.pop("host", None)
    
    # Inject user information into headers if authenticated
    if user_data:
        headers["X-User-ID"] = str(user_data.get("sub", ""))
        headers["X-User-Role"] = str(user_data.get("role", ""))
        headers["X-User-Department"] = str(user_data.get("department_id", ""))
    
    # Make the request to the target service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            
            # Return the response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type")
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Service unavailable: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=str(e)
            )
