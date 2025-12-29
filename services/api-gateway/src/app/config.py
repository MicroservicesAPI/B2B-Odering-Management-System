import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "API Gateway")
    VERSION = os.getenv("VERSION", "0.1.0")
    
    # Service URLs
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8002")
    PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8003")
    
    # JWT Configuration
    # WARNING: The default JWT_SECRET is insecure and should only be used for development.
    # In production, always set a strong, unique secret via environment variables.
    JWT_SECRET = os.getenv("JWT_SECRET", "Secret")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    
    # CORS Configuration
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")


config = Config()
