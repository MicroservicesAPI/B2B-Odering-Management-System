import pytest
from uuid import UUID
from app.schemas import OrderCreateRequest, OrderItemCreate
from app.services import OrderService
from app.db.models import OrderStatus


def test_create_order(db):
    """Test creating an order via service"""
    request = OrderCreateRequest(
        description="Service test order",
        items=[
            OrderItemCreate(product_name="Product A", quantity=5),
            OrderItemCreate(product_name="Product B", quantity=2)
        ]
    )
    
    user = {
        "sub": UUID("11111111-1111-1111-1111-111111111111"),
        "role": "staff",
        "department_id": 1
    }
    
    order = OrderService.create_order(db, request, user)
    
    assert order is not None
    assert order.user_id == user["sub"]
    assert order.department_id == user["department_id"]
    assert order.description == request.description
    assert len(order.items) == 2


def test_list_orders_as_admin(db):
    """Test listing all orders as admin"""
    # Create some test orders first
    request = OrderCreateRequest(
        description="Admin test order",
        items=[OrderItemCreate(product_name="Product X", quantity=1)]
    )
    
    user1 = {
        "sub": UUID("22222222-2222-2222-2222-222222222222"),
        "role": "staff",
        "department_id": 1
    }
    
    user2 = {
        "sub": UUID("33333333-3333-3333-3333-333333333333"),
        "role": "staff",
        "department_id": 2
    }
    
    OrderService.create_order(db, request, user1)
    OrderService.create_order(db, request, user2)
    
    # Admin should see all orders
    admin_user = {
        "sub": UUID("44444444-4444-4444-4444-444444444444"),
        "role": "admin",
        "department_id": 1
    }
    
    orders = OrderService.list_orders(db, admin_user)
    
    assert len(orders) >= 2


def test_list_orders_by_department(db):
    """Test listing orders filtered by department for non-admin users"""
    request = OrderCreateRequest(
        description="Department test order",
        items=[OrderItemCreate(product_name="Product Y", quantity=3)]
    )
    
    user_dept1 = {
        "sub": UUID("55555555-5555-5555-5555-555555555555"),
        "role": "staff",
        "department_id": 1
    }
    
    user_dept2 = {
        "sub": UUID("66666666-6666-6666-6666-666666666666"),
        "role": "staff",
        "department_id": 2
    }
    
    OrderService.create_order(db, request, user_dept1)
    OrderService.create_order(db, request, user_dept2)
    
    # Staff should only see their department's orders
    orders = OrderService.list_orders(db, user_dept1)
    
    assert all(order.department_id == 1 for order in orders)


def test_update_order_status_as_admin(db):
    """Test updating order status as admin"""
    request = OrderCreateRequest(
        description="Order to update status",
        items=[OrderItemCreate(product_name="Product Z", quantity=2)]
    )
    
    user = {
        "sub": UUID("77777777-7777-7777-7777-777777777777"),
        "role": "staff",
        "department_id": 1
    }
    
    order = OrderService.create_order(db, request, user)
    
    admin_user = {
        "sub": UUID("88888888-8888-8888-8888-888888888888"),
        "role": "admin",
        "department_id": 1
    }
    
    updated_order = OrderService.update_order_status(
        db, order.id, OrderStatus.APPROVED, admin_user
    )
    
    assert updated_order.status == OrderStatus.APPROVED


def test_update_order_status_as_non_admin_raises_error(db):
    """Test that non-admin users cannot update order status"""
    request = OrderCreateRequest(
        description="Order for status update test",
        items=[OrderItemCreate(product_name="Product W", quantity=1)]
    )
    
    user = {
        "sub": UUID("99999999-9999-9999-9999-999999999999"),
        "role": "staff",
        "department_id": 1
    }
    
    order = OrderService.create_order(db, request, user)
    
    # Try to update as non-admin (should raise ValueError)
    with pytest.raises(ValueError, match="Only admin can update order status"):
        OrderService.update_order_status(db, order.id, OrderStatus.APPROVED, user)


def test_update_nonexistent_order_raises_error(db):
    """Test that updating a non-existent order raises error"""
    admin_user = {
        "sub": UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        "role": "admin",
        "department_id": 1
    }
    
    fake_order_id = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    
    with pytest.raises(ValueError, match="Order not found"):
        OrderService.update_order_status(db, fake_order_id, OrderStatus.APPROVED, admin_user)
