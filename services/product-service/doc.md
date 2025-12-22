# Product Service (Warehouse Service)

## 📖 Overview
The Product Service is responsible for managing products stored in the central warehouse.  
It maintains the product catalog and tracks stock availability used by internal departments.

This service ensures inventory consistency and supports the internal ordering workflow.

---

## 🎯 Goals & Use Cases

### Goals
- Maintain a centralized warehouse inventory
- Track product stock levels
- Prevent invalid or over-ordering

### Use Cases
- Admin creates and updates products
- Staff views available products
- Order Service checks stock before approval

---

## 🏭 Warehouse Concept
- One central warehouse
- All products are stored in this warehouse
- Stock is deducted **only after order approval**

---

## 🧱 Data Model

### Product
| Field | Type | Description |
|------|----|------------|
| id | UUID | Product ID |
| name | String | Product name |
| sku | String | Stock keeping unit |
| description | String | Product description |
| stock_quantity | Integer | Available quantity |
| min_stock | Integer | Minimum stock threshold |
| created_at | Timestamp | Creation date |

---

## 🔌 Main Endpoints
| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /products | Create product (Admin) |
| GET | /products | List products |
| GET | /products/{id} | Get product details |
| PUT | /products/{id} | Update product |
| PATCH | /products/{id}/stock | Adjust stock level |

---

## 🔐 Access Control
- **Admin**: Full access (CRUD + stock updates)
- **Staff**: Read-only access

---

## 🛠 Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

---

## 🔒 Business Rules
- Stock cannot be negative
- Stock updates occur only via approved orders
- No direct DB access from other services

---

## 🚀 Run Locally
```bash
docker-compose up --build
