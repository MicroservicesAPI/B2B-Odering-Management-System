def test_create_product_route(client):
    """Test creating a product via API endpoint"""
    response = client.post(
        "/products",
        json={
            "name": "API Test Product",
            "sku": "API-TEST-001",
            "description": "Product created via API",
            "stock_quantity": 100,
            "min_stock": 10
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Test Product"
    assert data["sku"] == "API-TEST-001"
    assert data["stock_quantity"] == 100


def test_list_products_route(client):
    """Test listing products via API endpoint"""
    # Create some products first
    client.post(
        "/products",
        json={
            "name": "List Product 1",
            "sku": "LIST-API-001",
            "description": "First product",
            "stock_quantity": 50,
            "min_stock": 5
        }
    )

    client.post(
        "/products",
        json={
            "name": "List Product 2",
            "sku": "LIST-API-002",
            "description": "Second product",
            "stock_quantity": 75,
            "min_stock": 7
        }
    )

    # List products
    response = client.get("/products")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_product_by_id_route(client):
    """Test getting a product by ID via API endpoint"""
    # Create a product
    create_response = client.post(
        "/products",
        json={
            "name": "Get Test Product",
            "sku": "GET-API-001",
            "description": "Product to retrieve",
            "stock_quantity": 30,
            "min_stock": 3
        }
    )

    product_id = create_response.json()["id"]

    # Get the product
    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Get Test Product"


def test_update_product_route(client):
    """Test updating a product via API endpoint"""
    # Create a product
    create_response = client.post(
        "/products",
        json={
            "name": "Update Test Product",
            "sku": "UPDATE-API-001",
            "description": "Original description",
            "stock_quantity": 40,
            "min_stock": 4
        }
    )

    product_id = create_response.json()["id"]

    # Update the product
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Product Name",
            "description": "Updated description",
            "min_stock": 8
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product Name"
    assert data["description"] == "Updated description"
    assert data["min_stock"] == 8


def test_adjust_stock_route(client):
    """Test adjusting stock via API endpoint"""
    # Create a product
    create_response = client.post(
        "/products",
        json={
            "name": "Stock Adjust Product",
            "sku": "STOCK-API-001",
            "description": "Product for stock adjustment",
            "stock_quantity": 100,
            "min_stock": 10
        }
    )

    product_id = create_response.json()["id"]

    # Adjust stock
    response = client.patch(
        f"/products/{product_id}/stock",
        json={"quantity": 200}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["stock_quantity"] == 200


def test_create_product_staff_fails(client, db):
    """Test that staff cannot create products"""
    from app.routes import product_router, get_current_user
    from app.db import get_db
    from app.main import create_app
    from fastapi.testclient import TestClient

    # Override the current user to be staff
    def get_staff_user():
        return {
            "sub": "12345678-1234-5678-1234-567812345678",
            "role": "staff",
            "department_id": 1
        }

    # Create a new client with staff user
    app = create_app()
    app.router.lifespan_context = None

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = get_staff_user

    staff_client = TestClient(app)

    response = staff_client.post(
        "/products",
        json={
            "name": "Staff Product",
            "sku": "STAFF-001",
            "description": "Should fail",
            "stock_quantity": 10,
            "min_stock": 1
        }
    )

    # Should return 400 because user is not admin
    assert response.status_code == 400
    assert "Only admin" in response.json()["detail"]


def test_get_nonexistent_product_returns_404(client):
    """Test getting a nonexistent product returns 404"""
    response = client.get("/products/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Health check successful"


def test_duplicate_sku_returns_400(client):
    """Test that creating a product with duplicate SKU returns 400"""
    client.post(
        "/products",
        json={
            "name": "First Product",
            "sku": "DUPLICATE-SKU",
            "description": "First",
            "stock_quantity": 10,
            "min_stock": 1
        }
    )

    response = client.post(
        "/products",
        json={
            "name": "Second Product",
            "sku": "DUPLICATE-SKU",
            "description": "Second",
            "stock_quantity": 20,
            "min_stock": 2
        }
    )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]