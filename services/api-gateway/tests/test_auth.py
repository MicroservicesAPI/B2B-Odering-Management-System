import pytest
from jose import jwt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.auth import decode_token, get_current_user
from app.config import config
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials


def test_decode_valid_token():
    """Test decoding a valid token"""
    payload = {
        "sub": "12345678-1234-5678-1234-567812345678",
        "role": "staff",
        "department_id": "1",
        "type": "access"
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.ALGORITHM)
    
    decoded = decode_token(token)
    assert decoded["sub"] == payload["sub"]
    assert decoded["role"] == payload["role"]
    assert decoded["type"] == payload["type"]


def test_decode_invalid_token():
    """Test decoding an invalid token"""
    with pytest.raises(HTTPException) as exc_info:
        decode_token("invalid.token.here")
    
    assert exc_info.value.status_code == 401
    assert "Invalid or expired token" in exc_info.value.detail


def test_decode_token_wrong_secret():
    """Test decoding a token with wrong secret"""
    payload = {"sub": "123", "type": "access"}
    token = jwt.encode(payload, "wrong_secret", algorithm=config.ALGORITHM)
    
    with pytest.raises(HTTPException) as exc_info:
        decode_token(token)
    
    assert exc_info.value.status_code == 401


def test_get_current_user_valid():
    """Test getting current user with valid token"""
    payload = {
        "sub": "12345678-1234-5678-1234-567812345678",
        "role": "staff",
        "department_id": "1",
        "type": "access"
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.ALGORITHM)
    
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    user = get_current_user(credentials)
    
    assert user["sub"] == payload["sub"]
    assert user["role"] == payload["role"]
    assert user["type"] == payload["type"]


def test_get_current_user_refresh_token():
    """Test that refresh tokens are rejected for user authentication"""
    payload = {
        "sub": "12345678-1234-5678-1234-567812345678",
        "type": "refresh"
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.ALGORITHM)
    
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials)
    
    assert exc_info.value.status_code == 401
    assert "Invalid token type" in exc_info.value.detail
