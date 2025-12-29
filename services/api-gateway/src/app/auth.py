from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Dict, Optional

from app.config import config

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def decode_token(token: str) -> Dict:
    """
    Decode and validate JWT token
    """
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Extract and validate JWT token from Authorization header
    Returns the decoded user information
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type. Access token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security)) -> Optional[Dict]:
    """
    Extract JWT token if present, but don't require it
    Used for endpoints that work with or without authentication
    """
    if not credentials:
        return None
    
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None

