from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import config
from app.routes.auth import auth_router
from app.routes.orders import order_router
from app.routes.products import product_router


def create_app() -> FastAPI:
    """
    Create and configure the API Gateway application
    """
    app = FastAPI(
        title=config.PROJECT_NAME,
        version=config.VERSION,
        description="API Gateway for B2B Ordering Management System",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_router)
    app.include_router(order_router)
    app.include_router(product_router)
    
    @app.get("/")
    def health_check():
        """
        Health check endpoint
        """
        return JSONResponse(
            content={
                "status": "healthy",
                "service": "API Gateway",
                "version": config.VERSION
            }
        )
    
    @app.get("/health")
    def health():
        """
        Detailed health check endpoint
        """
        return JSONResponse(
            content={
                "status": "healthy",
                "service": "API Gateway",
                "version": config.VERSION,
                "services": {
                    "auth": config.AUTH_SERVICE_URL,
                    "orders": config.ORDER_SERVICE_URL,
                    "products": config.PRODUCT_SERVICE_URL
                }
            }
        )
    
    return app


app = create_app()
