from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import LoginRequest, RegisterRequest
from app.service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService.register(db, request)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        return AuthService.login(db, request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
