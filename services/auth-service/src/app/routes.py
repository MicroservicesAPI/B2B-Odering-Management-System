from fastapi import APIRouter

from app.schemas import LoginRequest, RegisterRequest

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login(request: LoginRequest):
    return {"message": "Login successful"}


@auth_router.post("/register")
async def register(request: RegisterRequest):
    return {"message": "Registration successful"}


@auth_router.get("/refresh_token")
def refresh_token():
    return {"message": "Refresh token successful"}
