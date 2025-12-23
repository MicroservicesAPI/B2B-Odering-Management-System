from fastapi import FastAPI

from app.config import app_config
from app.db import engine, Base, SQLALCHEMY_DATABASE_URL
from app.routes import auth_router


def create_app():
    auth_app = FastAPI(
        title=app_config.PROJECT_NAME,
        version=app_config.VERSION,
    )
    print(">>> DATABASE_URL =", SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    auth_app.include_router(auth_router)

    @auth_app.get("/health")
    def health():
        return {"message": "Health check successful"}

    return auth_app


app = create_app()
