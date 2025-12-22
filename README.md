# B2B-Odering-Management-System
Internal ordering system used by a small company to manage products, orders, and staff access.

---

## 📖 Overview
The Ordering Management System is a microservices-based application designed to manage product orders for an organization with multiple departments.  
It allows staff to create and track orders, while administrators manage users, departments, and order statuses. The system is modular, scalable, and designed for real-world use.

The system consists of the following services:
- **Auth Service**: Handles user authentication and role-based access.
- **Order Service**: Manages orders, order items, and status tracking.
- **API Gateway**: Single entry point for clients, handling routing, authentication, and request forwarding.
- *(Optional)* Warehouse Service: Manages inventory and stock levels.

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
  [API Gateway] -- validates JWT, routes requests
      |          \
      v           v
[Auth Service]   [Order Service]
                  |
                  v
             [Database]
