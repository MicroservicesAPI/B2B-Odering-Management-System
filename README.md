# B2B-Odering-Management-System
Internal ordering system used by a small company to manage products, orders, and staff access.

---

## 📖 Overview
The Ordering Management System is a microservices-based application designed to manage product orders for an organization with multiple departments.  
It allows staff to create and track orders, while administrators manage users, departments, and order statuses. The system is modular, scalable, and designed for real-world use.

The system consists of the following services:
- **API Gateway**: Single entry point for all clients, handling routing, JWT validation, and security.
- **Auth Service**: Handles user authentication, registration, and JWT token management.
- **Order Service**: Manages orders, order items, and status tracking.
- **Product Service**: Manages products and inventory with stock level tracking.

---

## 🎯 Goals & Use Cases

### Goals
- Provide a centralized ordering platform
- Enforce secure authentication and authorization
- Track orders by department and user
- Modular microservices architecture for scalability

### Use Cases
- Staff can create orders for their department
- Admin can view, approve, or cancel any order
- Users can view order history and status
- Gateway validates JWT tokens and forwards requests to services

---

## 🧩 Architecture

```text
[Frontend / Client]
        |
        v
  [API Gateway:8000] -- validates JWT, routes requests, CORS, security
      |       |        \
      v       v         v
[Auth:8001] [Order:8002] [Product:8003]
      |       |            |
      v       v            v
  [SQLite DB] [SQLite DB] [SQLite DB]
```

### Services
- **API Gateway** (Port 8000): Entry point for all client requests
  - JWT token validation
  - Request routing to backend services
  - CORS configuration
  - User information injection via headers
  
- **Auth Service** (Port 8001): User authentication and management
  - User registration and login
  - JWT token generation
  - Password hashing
  
- **Order Service** (Port 8002): Order management
  - Create and track orders
  - Order status management
  - Department-based access control
  
- **Product Service** (Port 8003): Product and inventory management
  - Product CRUD operations
  - Stock level tracking
  - Admin-only product management

---

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Access the API Gateway
# API Gateway: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Running Locally (Development)

```bash
# Install dependencies for each service
cd services/api-gateway && pip install -r requirements.txt
cd services/auth-service && pip install -r requirements.txt
cd services/order-service && pip install -r requirements.txt
cd services/product-service && pip install -r requirements.txt

# Run each service in separate terminals
cd services/api-gateway && python run.py
cd services/auth-service && LOCAL_RUN=1 python run.py
cd services/order-service && LOCAL_RUN=1 python run.py
cd services/product-service && LOCAL_RUN=1 python run.py
```

### Running Tests

```bash
# Run tests for API Gateway
cd services/api-gateway && pytest tests/ -v

# Run tests for Auth Service
cd services/auth-service && LOCAL_RUN=1 pytest tests/ -v

# Run tests for Order Service
cd services/order-service && LOCAL_RUN=1 pytest tests/ -v

# Run tests for Product Service
cd services/product-service && LOCAL_RUN=1 pytest tests/ -v
```

---

## 🔒 Security Features

The API Gateway implements several security measures:

1. **JWT Authentication**: All protected endpoints require valid JWT access tokens
2. **Token Validation**: Tokens are validated for signature, expiration, and type
3. **User Context Injection**: User information is extracted from JWT and passed to backend services via headers
4. **CORS Configuration**: Cross-Origin Resource Sharing is properly configured
5. **Role-Based Access Control**: Different user roles (admin, staff) have different permissions

### Authentication Flow

1. Client sends login request to `/auth/login` via API Gateway
2. Gateway forwards request to Auth Service
3. Auth Service validates credentials and returns JWT tokens
4. Client includes access token in subsequent requests via Authorization header
5. Gateway validates token and injects user info into headers
6. Backend services use user info from headers for authorization

---

## 📚 API Documentation

Once the services are running, access the interactive API documentation:

- **API Gateway**: http://localhost:8000/docs
- **Auth Service** (direct): http://localhost:8001/docs
- **Order Service** (direct): http://localhost:8002/docs
- **Product Service** (direct): http://localhost:8003/docs

**Note**: In production, only the API Gateway should be exposed to clients.

---

## 🛠 Technology Stack

- **Framework**: FastAPI
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **ORM**: SQLAlchemy
- **HTTP Client**: httpx (for service-to-service communication)
- **Testing**: pytest
- **Containerization**: Docker

---
