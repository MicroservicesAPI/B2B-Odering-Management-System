from uuid import UUID


def test_create_order_route(client):
    """Test creating an order via API endpoint"""
    response = client.post(
        "/orders",
        json={
            "description": "API test order",
            "items": [
                {"product_name": "Product A", "quantity": 5},
                {"product_name": "Product B", "quantity": 3}
            ]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "API test order"
    assert len(data["items"]) == 2
    assert data["status"] == "pending"


def test_list_orders_route(client):
    """Test listing orders via API endpoint"""
    # Create some orders first
    client.post(
        "/orders",
        json={
            "description": "List test order 1",
            "items": [{"product_name": "Product X", "quantity": 1}]
        }
    )
    
    client.post(
        "/orders",
        json={
            "description": "List test order 2",
            "items": [{"product_name": "Product Y", "quantity": 2}]
        }
    )
    
    # List orders
    response = client.get("/orders")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_order_status_route_requires_admin(client, db):
    """Test that updating order status requires admin role"""
    # Create an order first
    create_response = client.post(
        "/orders",
        json={
            "description": "Order for status update",
            "items": [{"product_name": "Product Z", "quantity": 1}]
        }
    )
    
    order_id = create_response.json()["id"]
    
    # Try to update status (will fail because default user is staff, not admin)
    from app.routes import order_router, get_current_user
    from app.db import get_db
    
    # Override the current user to be staff (non-admin)
    def get_staff_user():
        return {
            "sub": "12345678-1234-5678-1234-567812345678",
            "role": "staff",
            "department_id": 1
        }
    
    # Create a new client with staff user
    from app.main import create_app
    from fastapi.testclient import TestClient
    
    app = create_app()
    app.router.lifespan_context = None
    
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = get_staff_user
    
    staff_client = TestClient(app)
    
    response = staff_client.put(
        f"/orders/{order_id}/status",
        params={"status": "approved"}
    )
    
    # Should return 403 because user is not admin
    assert response.status_code == 403
    assert "Only admin can update order status" in response.json()["detail"]


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Health check successful"
