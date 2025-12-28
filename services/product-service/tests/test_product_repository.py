from uuid import UUID
from app.product_repository import ProductRepository


def test_create_and_get_product(db):
    """Test creating a product and retrieving it by ID"""
    product = ProductRepository.create_product(
        db=db,
        name="Test Product A",
        sku="TEST-SKU-001",
        description="A test product",
        stock_quantity=100,
        min_stock=10
    )

    assert product is not None
    assert product.name == "Test Product A"
    assert product.sku == "TEST-SKU-001"
    assert product.description == "A test product"
    assert product.stock_quantity == 100
    assert product.min_stock == 10

    # Fetch the created product by ID
    fetched = ProductRepository.get_by_id(db, product.id)

    assert fetched is not None
    assert fetched.id == product.id
    assert fetched.name == "Test Product A"


def test_get_by_sku(db):
    """Test retrieving a product by SKU"""
    product = ProductRepository.create_product(
        db=db,
        name="Product B",
        sku="TEST-SKU-002",
        description="Another product",
        stock_quantity=50,
        min_stock=5
    )

    fetched = ProductRepository.get_by_sku(db, "TEST-SKU-002")

    assert fetched is not None
    assert fetched.id == product.id
    assert fetched.sku == "TEST-SKU-002"


def test_duplicate_sku_raises_error(db):
    """Test that creating a product with duplicate SKU raises an error"""
    ProductRepository.create_product(
        db=db,
        name="Product C",
        sku="DUPLICATE-SKU",
        description="First product",
        stock_quantity=20,
        min_stock=2
    )

    # Try to create another product with the same SKU
    try:
        ProductRepository.create_product(
            db=db,
            name="Product D",
            sku="DUPLICATE-SKU",
            description="Second product",
            stock_quantity=30,
            min_stock=3
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already exists" in str(e)


def test_list_all_products(db):
    """Test listing all products"""
    ProductRepository.create_product(
        db=db,
        name="Product E",
        sku="TEST-SKU-005",
        description="Product for listing",
        stock_quantity=15,
        min_stock=1
    )

    all_products = ProductRepository.list_all(db)

    assert len(all_products) > 0
    assert any(product.sku == "TEST-SKU-005" for product in all_products)


def test_update_product(db):
    """Test updating product details"""
    product = ProductRepository.create_product(
        db=db,
        name="Product F",
        sku="TEST-SKU-006",
        description="Original description",
        stock_quantity=25,
        min_stock=5
    )

    updated = ProductRepository.update_product(
        db=db,
        product=product,
        name="Updated Product F",
        description="Updated description",
        min_stock=10
    )

    assert updated.name == "Updated Product F"
    assert updated.description == "Updated description"
    assert updated.min_stock == 10
    assert updated.stock_quantity == 25  # Stock should not change


def test_adjust_stock(db):
    """Test adjusting stock quantity"""
    product = ProductRepository.create_product(
        db=db,
        name="Product G",
        sku="TEST-SKU-007",
        description="Product for stock adjustment",
        stock_quantity=100,
        min_stock=10
    )

    # Adjust stock to 150
    updated = ProductRepository.adjust_stock(db, product, 150)

    assert updated.stock_quantity == 150

    # Verify the update persisted
    fetched = ProductRepository.get_by_id(db, product.id)
    assert fetched.stock_quantity == 150


def test_adjust_stock_negative_raises_error(db):
    """Test that adjusting stock to negative value raises an error"""
    product = ProductRepository.create_product(
        db=db,
        name="Product H",
        sku="TEST-SKU-008",
        description="Product for negative stock test",
        stock_quantity=50,
        min_stock=5
    )

    try:
        ProductRepository.adjust_stock(db, product, -10)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be negative" in str(e)


def test_delete_product(db):
    """Test deleting a product"""
    product = ProductRepository.create_product(
        db=db,
        name="Product I",
        sku="TEST-SKU-009",
        description="Product to delete",
        stock_quantity=10,
        min_stock=1
    )

    product_id = product.id

    ProductRepository.delete_product(db, product)

    # Verify the product is deleted
    fetched = ProductRepository.get_by_id(db, product_id)
    assert fetched is None