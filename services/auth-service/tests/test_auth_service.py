from uuid import UUID

import pytest
from app.schemas import RegisterRequest, LoginRequest, UserRole
from app.service import AuthService


def test_register_user(db):
    request = RegisterRequest(
        email="register@test.com",
        password="password123",
        name="Register Test",
        role=UserRole.STAFF,
        department_id=UUID("22222222-2222-2222-2222-222222222222")
    )

    user = AuthService.register(db, request)

    assert user.email == request.email
    assert user.name == request.name


def test_login_user(db):
    register_request = RegisterRequest(
        email="login@test.com",
        password="password123",
        name="Login Test",
        role=UserRole.STAFF,
        department_id=UUID("33333333-3333-3333-3333-333333333333")
    )

    AuthService.register(db, register_request)

    login_request = LoginRequest(
        email="login@test.com",
        password="password123"
    )

    response = AuthService.login(db, login_request)

    assert "access_token" in response
    assert "refresh_token" in response
    assert response["token_type"] == "bearer"


def test_login_invalid_password(db):
    register_request = RegisterRequest(
        email="fail@test.com",
        password="password123",
        name="Fail Test",
        role=UserRole.STAFF,
        department_id=UUID("44444444-4444-4444-4444-444444444444")
    )

    AuthService.register(db, register_request)

    login_request = LoginRequest(
        email="fail@test.com",
        password="wrongpassword"
    )

    with pytest.raises(ValueError):
        AuthService.login(db, login_request)
