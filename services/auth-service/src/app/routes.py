from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/login")
def login():
    return {"message": "Login successful"}


@auth_router.post("/register")
def register():
    return {"message": "Registration successful"}


@auth_router.get("/refresh token")
def refresh_token():
    return {"message": "Refresh token successful"}
