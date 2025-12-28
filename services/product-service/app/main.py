from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import app_config
from app.db import engine, Base, SQLALCHEMY_DATABASE_URL
#from app.routes import product_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    Base.metadata.create_all(bind=engine)
    yield  # the app run here

    # SHUTDOWN (optional)
    # engine.dispose()

def create_app():
    product_app = FastAPI(
        title=app_config.PROJECT_NAME,
        version=app_config.VERSION,
        lifespan=lifespan
    )

    print(">>> DATABASE_URL =", SQLALCHEMY_DATABASE_URL)
    #product_app.include_router(product_router)

    @product_app.get("/")
    def health():
        return {"message": "Health check successful"}

    return product_app