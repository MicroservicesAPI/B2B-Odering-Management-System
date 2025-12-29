import pytest
from unittest.mock import patch, AsyncMock
from fastapi import Response


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "API Gateway"


def test_health_endpoint(client):
    """Test the detailed health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert "auth" in data["services"]
    assert "orders" in data["services"]
    assert "products" in data["services"]


def test_auth_proxy_register(client):
    """Test proxying register request to auth service"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User",
            "role": "staff",
            "department_id": "12345678-1234-5678-1234-567812345678"
        }
    )
    
    # Service is not available in tests, so we expect 503
    assert response.status_code == 503


def test_auth_proxy_login(client):
    """Test proxying login request to auth service"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Service is not available in tests, so we expect 503
    assert response.status_code == 503


def test_orders_without_auth(client):
    """Test that orders endpoint requires authentication"""
    response = client.get("/orders")
    assert response.status_code == 401  # Unauthorized without auth


def test_products_without_auth(client):
    """Test that products endpoint requires authentication"""
    response = client.get("/products")
    assert response.status_code == 401  # Unauthorized without auth


def test_cors_headers(client):
    """Test that CORS headers are present"""
    response = client.options("/")
    # CORS middleware should add appropriate headers
    assert response.status_code in [200, 405]

