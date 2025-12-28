from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import Product


class ProductRepository:

    @staticmethod
    def create_product(
        db: Session,
        name: str,
        sku: str,
        description: str | None,
        stock_quantity: int,
        min_stock: int
    ) -> Product:
        """Create a new product"""
        product = Product(
            name=name,
            sku=sku,
            description=description,
            stock_quantity=stock_quantity,
            min_stock=min_stock
        )
        
        try:
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Product with SKU '{sku}' already exists")

    @staticmethod
    def get_by_id(db: Session, product_id) -> Product | None:
        """Get product by ID"""
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_by_sku(db: Session, sku: str) -> Product | None:
        """Get product by SKU"""
        return db.query(Product).filter(Product.sku == sku).first()

    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100):
        """List all products with pagination"""
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def update_product(
        db: Session,
        product: Product,
        name: str | None = None,
        description: str | None = None,
        min_stock: int | None = None
    ) -> Product:
        """Update product details"""
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if min_stock is not None:
            product.min_stock = min_stock
        
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def adjust_stock(db: Session, product: Product, new_quantity: int) -> Product:
        """Adjust stock quantity"""
        if new_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        product.stock_quantity = new_quantity
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product: Product):
        """Delete a product"""
        db.delete(product)
        db.commit()
