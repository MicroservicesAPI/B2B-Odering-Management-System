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
