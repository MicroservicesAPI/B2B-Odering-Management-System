# API Gateway

## 📖 Overview
The API Gateway is the single entry point for all clients to access the microservices in the B2B Ordering Management System. It handles authentication, request routing, and security for the entire system.

## 🎯 Features

### Core Functionality
- **JWT Authentication**: Validates access tokens on protected endpoints
- **Request Routing**: Forwards requests to appropriate backend services
- **User Context Injection**: Extracts user information from JWT and passes it to services via headers
- **CORS Support**: Configurable cross-origin resource sharing
- **Health Checks**: Monitoring endpoints for service health

### Security Features
- JWT token validation with proper algorithm verification
- Token type checking (access vs refresh tokens)
- Automatic user context propagation to backend services
- Secure header injection for service-to-service communication

## 🔌 Endpoints

### Health & Status
- `GET /` - Basic health check
- `GET /health` - Detailed health check with service URLs

### Authentication (Proxied to Auth Service)
All `/auth/*` endpoints are forwarded to the Auth Service:
- `POST /auth/register` - User registration (no auth required)
- `POST /auth/login` - User login (no auth required)
- `POST /auth/refresh` - Refresh access token (no auth required)
- `GET /auth/me` - Get current user info (auth required)

### Orders (Proxied to Order Service)
All `/orders/*` endpoints require authentication:
- `POST /orders` - Create a new order
- `GET /orders` - List orders (filtered by role/department)
- `GET /orders/{id}` - Get order details
- `PUT /orders/{id}/status` - Update order status (admin only)

### Products (Proxied to Product Service)
All `/products/*` endpoints require authentication:
- `POST /products` - Create a product (admin only)
- `GET /products` - List all products
- `GET /products/{id}` - Get product details
- `PUT /products/{id}` - Update product (admin only)
- `PATCH /products/{id}/stock` - Adjust stock level (admin only)

## 🔒 Authentication Flow

### Login
```bash
# 1. Login to get tokens
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Response:
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Making Authenticated Requests
```bash
# 2. Use access token for protected endpoints
curl -X GET http://localhost:8000/orders \
  -H "Authorization: Bearer eyJhbGc..."
```

### Token Validation
The gateway validates:
1. **Token signature**: Ensures token was signed with correct secret
2. **Token expiration**: Checks if token is still valid
3. **Token type**: Ensures access tokens are used (not refresh tokens)

### User Context Propagation
When a valid token is provided, the gateway extracts user information and adds it to headers:
- `X-User-ID`: User's unique identifier
- `X-User-Role`: User's role (admin/staff)
- `X-User-Department`: User's department ID

Backend services can use these headers to enforce authorization rules.

## 🛠 Configuration

Environment variables (see `.env.example`):

```bash
# Service URLs
AUTH_SERVICE_URL=http://auth-service:8001
ORDER_SERVICE_URL=http://order-service:8002
PRODUCT_SERVICE_URL=http://product-service:8003

# JWT Configuration
JWT_SECRET=your-secret-key
ALGORITHM=HS256

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🚀 Running the Service

### With Docker
```bash
docker-compose up api-gateway
```

### Locally (Development)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python run.py

# The gateway will be available at http://localhost:8000
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 📊 Architecture

```
[Client Request]
      |
      v
[API Gateway]
      |
      |-- Validate JWT (if required)
      |-- Extract user info from token
      |-- Add user headers (X-User-ID, X-User-Role, X-User-Department)
      |-- Route request
      v
[Backend Service]
      |
      |-- Read user info from headers
      |-- Apply authorization rules
      |-- Process request
      v
[Response to Client]
```

## 🔧 Development

### Adding a New Route
To proxy a new backend service:

1. Create a new route file in `app/routes/`:
```python
from fastapi import APIRouter, Request, Depends
from app.auth import get_current_user
from app.config import config
from app.proxy import forward_request

my_router = APIRouter(prefix="/myservice", tags=["myservice"])

@my_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_my_service(path: str, request: Request, user = Depends(get_current_user)):
    target_url = f"{config.MY_SERVICE_URL}/myservice/{path}"
    return await forward_request(request, target_url, user)
```

2. Register the router in `app/main.py`:
```python
from app.routes.myservice import my_router
app.include_router(my_router)
```

3. Add service URL to config and environment variables

### Debugging
Enable debug logging by setting log level:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Security Best Practices

1. **Never expose JWT secret**: Keep `JWT_SECRET` secure and rotate regularly
2. **Use HTTPS in production**: All traffic should be encrypted
3. **Validate token expiration**: Tokens should have reasonable expiration times
4. **Rate limiting**: Consider adding rate limiting for production
5. **Monitor logs**: Watch for suspicious authentication patterns

## 📝 Notes

- The gateway does NOT store any data
- All requests are stateless
- JWT secret must match the Auth Service secret
- Backend services should trust headers from the gateway but validate for direct access
- In production, only the gateway should be publicly accessible

## 🐛 Troubleshooting

### "Service unavailable" errors
- Check that backend services are running
- Verify service URLs in configuration
- Check network connectivity between services

### "Invalid or expired token" errors
- Verify JWT_SECRET matches Auth Service
- Check token expiration time
- Ensure correct token type (access vs refresh)

### CORS errors
- Update ALLOWED_ORIGINS in configuration
- Ensure frontend is using correct origin

## 📚 Related Documentation
- [Auth Service Documentation](../auth-service/doc.md)
- [Order Service Documentation](../order-service/doc.md)
- [Product Service Documentation](../product-service/doc.md)
