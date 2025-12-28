from sqlalchemy.orm import Session

from app.product_repository import ProductRepository
from app.schemas import ProductCreate, ProductUpdate, StockAdjustment


class ProductService:

    @staticmethod
    def create_product(db: Session, request: ProductCreate, user: dict):
        """
        Create a new product (Admin only)
        """
        if user["role"] != "admin":
            raise ValueError("Only admin can create products")
        
        return ProductRepository.create_product(
            db=db,
            name=request.name,
            sku=request.sku,
            description=request.description,
            stock_quantity=request.stock_quantity,
            min_stock=request.min_stock
        )

    @staticmethod
    def get_product(db: Session, product_id: str, user: dict):
        """
        Get product details (Admin and Staff)
        """
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")
        return product

    @staticmethod
    def list_products(db: Session, user: dict, skip: int = 0, limit: int = 100):
        """
        List all products (Admin and Staff)
        """
        return ProductRepository.list_all(db, skip=skip, limit=limit)

    @staticmethod
    def update_product(db: Session, product_id: str, request: ProductUpdate, user: dict):
        """
        Update product details (Admin only)
        """
        if user["role"] != "admin":
            raise ValueError("Only admin can update products")
        
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")
        
        return ProductRepository.update_product(
            db=db,
            product=product,
            name=request.name,
            description=request.description,
            min_stock=request.min_stock
        )

    @staticmethod
    def adjust_stock(db: Session, product_id: str, request: StockAdjustment, user: dict):
        """
        Adjust stock quantity (Admin only)
        """
        if user["role"] != "admin":
            raise ValueError("Only admin can adjust stock")
        
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")
        
        return ProductRepository.adjust_stock(
            db=db,
            product=product,
            new_quantity=request.quantity
        )
