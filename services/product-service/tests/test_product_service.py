from uuid import UUID
from app.service import ProductService
from app.schemas import ProductCreate, ProductUpdate, StockAdjustment
from app.product_repository import ProductRepository


def test_create_product_as_admin(db):
    """Test creating a product as admin"""
    admin_user = {
        "sub": "admin-uuid",
        "role": "admin",
        "department_id": 1
    }

    request = ProductCreate(
        name="Service Test Product",
        sku="SVC-TEST-001",
        description="Test via service",
        stock_quantity=50,
        min_stock=5
    )

    product = ProductService.create_product(db, request, admin_user)

    assert product is not None
    assert product.name == "Service Test Product"
    assert product.sku == "SVC-TEST-001"


def test_create_product_as_staff_fails(db):
    """Test that staff cannot create products"""
    staff_user = {
        "sub": "staff-uuid",
        "role": "staff",
        "department_id": 1
    }

    request = ProductCreate(
        name="Staff Product",
        sku="STAFF-001",
        description="Should fail",
        stock_quantity=10,
        min_stock=1
    )

    try:
        ProductService.create_product(db, request, staff_user)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Only admin" in str(e)


def test_get_product_as_staff(db):
    """Test that staff can view products"""
    # Create a product first
    admin_user = {
        "sub": "admin-uuid",
        "role": "admin",
        "department_id": 1
    }

    product = ProductRepository.create_product(
        db=db,
        name="View Test Product",
        sku="VIEW-TEST-001",
        description="For viewing",
        stock_quantity=100,
        min_stock=10
    )

    # Staff can view
    staff_user = {
        "sub": "staff-uuid",
        "role": "staff",
        "department_id": 1
    }

    fetched = ProductService.get_product(db, str(product.id), staff_user)
    assert fetched is not None
    assert fetched.name == "View Test Product"


def test_list_products_as_staff(db):
    """Test that staff can list products"""
    staff_user = {
        "sub": "staff-uuid",
        "role": "staff",
        "department_id": 1
    }

    # Create some products
    ProductRepository.create_product(
        db=db,
        name="List Product 1",
        sku="LIST-001",
        description="First",
        stock_quantity=10,
        min_stock=1
    )

    ProductRepository.create_product(
        db=db,
        name="List Product 2",
        sku="LIST-002",
        description="Second",
        stock_quantity=20,
        min_stock=2
    )

    products = ProductService.list_products(db, staff_user)

    assert len(products) >= 2


def test_update_product_as_admin(db):
    """Test updating a product as admin"""
    admin_user = {
        "sub": "admin-uuid",
        "role": "admin",
        "department_id": 1
    }

    # Create a product
    product = ProductRepository.create_product(
        db=db,
        name="Update Test",
        sku="UPDATE-001",
        description="Original",
        stock_quantity=50,
        min_stock=5
    )

    # Update it
    update_request = ProductUpdate(
        name="Updated Name",
        description="Updated description",
        min_stock=10
    )

    updated = ProductService.update_product(
        db, str(product.id), update_request, admin_user
    )

    assert updated.name == "Updated Name"
    assert updated.description == "Updated description"
    assert updated.min_stock == 10


def test_update_product_as_staff_fails(db):
    """Test that staff cannot update products"""
    staff_user = {
        "sub": "staff-uuid",
        "role": "staff",
        "department_id": 1
    }

    # Create a product
    product = ProductRepository.create_product(
        db=db,
        name="Staff Update Test",
        sku="STAFF-UPDATE-001",
        description="Original",
        stock_quantity=50,
        min_stock=5
    )

    update_request = ProductUpdate(name="Should Fail")

    try:
        ProductService.update_product(
            db, str(product.id), update_request, staff_user
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Only admin" in str(e)


def test_adjust_stock_as_admin(db):
    """Test adjusting stock as admin"""
    admin_user = {
        "sub": "admin-uuid",
        "role": "admin",
        "department_id": 1
    }

    # Create a product
    product = ProductRepository.create_product(
        db=db,
        name="Stock Adjust Test",
        sku="STOCK-001",
        description="For stock adjustment",
        stock_quantity=100,
        min_stock=10
    )

    # Adjust stock
    adjustment = StockAdjustment(quantity=150)

    updated = ProductService.adjust_stock(
        db, str(product.id), adjustment, admin_user
    )

    assert updated.stock_quantity == 150


def test_adjust_stock_as_staff_fails(db):
    """Test that staff cannot adjust stock"""
    staff_user = {
        "sub": "staff-uuid",
        "role": "staff",
        "department_id": 1
    }

    # Create a product
    product = ProductRepository.create_product(
        db=db,
        name="Staff Stock Test",
        sku="STAFF-STOCK-001",
        description="For staff stock test",
        stock_quantity=100,
        min_stock=10
    )

    adjustment = StockAdjustment(quantity=50)

    try:
        ProductService.adjust_stock(
            db, str(product.id), adjustment, staff_user
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Only admin" in str(e)


def test_get_nonexistent_product_fails(db):
    """Test that getting a nonexistent product raises an error"""
    admin_user = {
        "sub": "admin-uuid",
        "role": "admin",
        "department_id": 1
    }

    try:
        ProductService.get_product(
            db, "00000000-0000-0000-0000-000000000000", admin_user
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "not found" in str(e)