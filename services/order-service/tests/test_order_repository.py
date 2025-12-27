from uuid import UUID
from app.order_repository import OrderRepository
from app.schemas import OrderItemCreate
from app.db.models import OrderStatus


def test_create_and_get_order(db):
    """Test creating an order and retrieving it by ID"""
    items = [
        OrderItemCreate(product_name="Product A", quantity=5),
        OrderItemCreate(product_name="Product B", quantity=3)
    ]
    
    order = OrderRepository.create_order(
        db=db,
        user_id=UUID("11111111-1111-1111-1111-111111111111"),
        department_id=1,
        description="Test order",
        items=items
    )
    
    assert order is not None
    assert order.user_id == UUID("11111111-1111-1111-1111-111111111111")
    assert order.department_id == 1
    assert order.description == "Test order"
    assert order.status == OrderStatus.PENDING
    assert len(order.items) == 2
    
    # Fetch the created order
    fetched = OrderRepository.get_by_id(db, order.id)
    
    assert fetched is not None
    assert fetched.id == order.id
    assert fetched.description == "Test order"
    assert len(fetched.items) == 2


def test_list_by_department(db):
    """Test listing orders by department"""
    items = [OrderItemCreate(product_name="Product C", quantity=2)]
    
    # Create orders for different departments
    OrderRepository.create_order(
        db=db,
        user_id=UUID("22222222-2222-2222-2222-222222222222"),
        department_id=1,
        description="Dept 1 Order 1",
        items=items
    )
    
    OrderRepository.create_order(
        db=db,
        user_id=UUID("33333333-3333-3333-3333-333333333333"),
        department_id=1,
        description="Dept 1 Order 2",
        items=items
    )
    
    OrderRepository.create_order(
        db=db,
        user_id=UUID("44444444-4444-4444-4444-444444444444"),
        department_id=2,
        description="Dept 2 Order 1",
        items=items
    )
    
    # List orders for department 1
    dept1_orders = OrderRepository.list_by_department(db, department_id=1)
    
    assert len(dept1_orders) >= 2
    assert all(order.department_id == 1 for order in dept1_orders)


def test_list_all_orders(db):
    """Test listing all orders"""
    items = [OrderItemCreate(product_name="Product D", quantity=1)]
    
    OrderRepository.create_order(
        db=db,
        user_id=UUID("55555555-5555-5555-5555-555555555555"),
        department_id=3,
        description="Order for all test",
        items=items
    )
    
    all_orders = OrderRepository.list_all(db)
    
    assert len(all_orders) > 0
    assert any(order.description == "Order for all test" for order in all_orders)


def test_update_order_status(db):
    """Test updating order status"""
    items = [OrderItemCreate(product_name="Product E", quantity=4)]
    
    order = OrderRepository.create_order(
        db=db,
        user_id=UUID("66666666-6666-6666-6666-666666666666"),
        department_id=4,
        description="Order to update",
        items=items
    )
    
    assert order.status == OrderStatus.PENDING
    
    # Update status to APPROVED
    updated_order = OrderRepository.update_status(db, order, OrderStatus.APPROVED)
    
    assert updated_order.status == OrderStatus.APPROVED
    assert updated_order.id == order.id
    
    # Verify the update persisted
    fetched = OrderRepository.get_by_id(db, order.id)
    assert fetched.status == OrderStatus.APPROVED
