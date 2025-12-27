# Order Service

## 📖 Overview
The Order Service is responsible for managing internal orders placed by company departments to request products from the central warehouse.

It handles the full order lifecycle, including creation, approval, rejection, and delivery, while enforcing business rules.

This service collaborates closely with the Product Service and Notification Service.

---

## 🎯 Goals & Use Cases

### Goals
- Enable departments to request products from the warehouse
- Track the complete order lifecycle
- Enforce approval and delivery workflows
- Ensure stock consistency through controlled state transitions

### Use Cases
- Staff creates an order request
- Admin reviews and approves or rejects orders
- Approved orders trigger stock deduction
- Departments track order status

---

## 🏢 Ordering Concept
- Orders are created by **department staff**
- Orders are reviewed by **warehouse admins**
- Stock is deducted **only after approval**
- Each order belongs to exactly **one department**

---

## 🔄 Order Lifecycle

---

## 🧪 Testing

### Running Tests

The order service has comprehensive unit tests covering the repository, service, and API layers.

#### Prerequisites
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (copy `.env.example` to `.env`):
```bash
cp .env.example .env
```

#### Run All Tests
```bash
python -m pytest tests/ -v
```

#### Run Specific Test Files
```bash
# Repository tests
python -m pytest tests/test_order_repository.py -v

# Service tests
python -m pytest tests/test_order_service.py -v

# Routes/API tests
python -m pytest tests/test_order_routes.py -v
```

#### Test Coverage
- **Repository Layer**: 4 tests covering CRUD operations
- **Service Layer**: 6 tests covering business logic and permissions
- **API Layer**: 4 tests covering HTTP endpoints

All tests use SQLite for the test database to ensure fast, isolated test runs.
