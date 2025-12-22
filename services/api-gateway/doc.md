# API Gateway

## 📖 Overview
The API Gateway is the single entry point for all clients to access the microservices.  
It routes requests to the appropriate service (Auth Service, Order Service) and handles authentication, logging, and error handling.

This service centralizes external communication and ensures consistent security and access control across the system.

---

## 🎯 Goals & Use Cases

### Goals
- Centralize API access for all services
- Validate JWT access tokens from Auth Service
- Simplify frontend integration
- Enforce role-based access control

### Use Cases
- Proxy login/register requests to Auth Service
- Proxy order requests to Order Service
- Validate user tokens
- Handle service errors consistently

---

## 🔌 Main Endpoints
| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /auth/register | Forward to Auth Service |
| POST | /auth/login | Forward to Auth Service |
| POST | /auth/refresh | Forward to Auth Service |
| GET  | /auth/me | Forward to Auth Service |
| POST | /orders | Forward to Order Service |
| GET  | /orders | Forward to Order Service |
| GET  | /orders/me | Forward to Order Service |
| PUT  | /orders/{id} | Forward to Order Service |
| GET  | /orders/{id} | Forward to Order Service |

---

## 🛠 Tech Stack
- FastAPI
- Uvicorn
- JWT middleware
- Docker

---

## 🔒 Security Notes
- All incoming requests validated with JWT
- Role-based access enforced via Auth Service
- No direct database access from gateway

---

## 🚀 Run Locally
```bash
docker-compose up --build
