import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.main import create_app


@pytest.fixture
def client():
    """Create a test client"""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_auth_token():
    """Create a mock JWT token"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3OC0xMjM0LTU2NzgtMTIzNC01Njc4MTIzNDU2NzgiLCJyb2xlIjoic3RhZmYiLCJkZXBhcnRtZW50X2lkIjoiMSIsInR5cGUiOiJhY2Nlc3MifQ"
