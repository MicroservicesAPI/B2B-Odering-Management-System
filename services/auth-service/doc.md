# Auth Service

## 📖 Overview
The Auth Service is responsible for user authentication and authorization across the system.  
It provides secure login, token management, and role-based access control for internal users.

This service is a core component of the architecture and is consumed by the API Gateway and other services.

---

## 🎯 Goals & Use Cases

### Goals
- Centralize authentication logic
- Secure all services using JWT
- Enforce role-based access (Admin, Staff)

### Use Cases
- User registration
- User login
- Token refresh
- Role verification for protected endpoints

---

## 👤 User Roles
- **Admin**: Warehouse administrator with full access
- **Staff**: Department user with limited permissions

---

## 🔐 Authentication Flow
1. User logs in with email and password
2. Auth Service validates credentials
3. JWT access & refresh tokens are issued
4. API Gateway validates tokens on incoming requests

---

## 🧱 Data Model

### User
| Field | Type | Description |
|------|----|------------|
| id | UUID | Unique user ID |
| email | String | User email |
| password_hash | String | Hashed password |
| role | Enum | ADMIN / STAFF |
| department_id | UUID | Linked department |
| is_active | Boolean | Account status |
| created_at | Timestamp | Creation date |

### Department
| Field | Type | Description |
|------|----|------------|
| id | UUID | Department ID |
| name | String | Department name |

---

## 🔌 Main Endpoints
| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | User login |
| POST | /auth/refresh | Refresh JWT |
| GET | /auth/me | Get current user |

---

## 🛠 Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (Access & Refresh)
- Docker

---

## 🔒 Security Notes
- Passwords are hashed (bcrypt)
- Tokens are signed and time-limited
- No direct DB access from other services

---

## 🚀 Run Locally
```bash
docker-compose up --build

