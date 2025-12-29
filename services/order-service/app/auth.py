"""
Utility to extract user information from request headers
This is used when requests come through the API Gateway
"""
from fastapi import Header, HTTPException
from typing import Optional

# Default values for development/testing
DEFAULT_USER_ID = "12345678-1234-5678-1234-567812345678"
DEFAULT_DEPARTMENT_ID = "1"


def get_current_user(
    x_user_id: Optional[str] = Header(None),
    x_user_role: Optional[str] = Header(None),
    x_user_department: Optional[str] = Header(None)
):
    """
    Extract user information from headers injected by API Gateway
    Falls back to mock user for direct service access (development/testing)
    """
    if x_user_id and x_user_role:
        # User info from gateway
        return {
            "sub": x_user_id,
            "role": x_user_role,
            "department_id": x_user_department or DEFAULT_DEPARTMENT_ID
        }
    else:
        # Mock user for direct access (development/testing)
        return {
            "sub": DEFAULT_USER_ID,
            "role": "staff",
            "department_id": DEFAULT_DEPARTMENT_ID
        }
