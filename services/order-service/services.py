from sqlalchemy.orm import Session

from app.order_repository import OrderRepository
from app.db.models import OrderStatus


class OrderService:

    @staticmethod
    def create_order(db: Session, request, user):
        """
        user comes from JWT (gateway or dependency)
        """
        return OrderRepository.create_order(
            db=db,
            user_id=user["sub"],
            department_id=user["department_id"],
            description=request.description,
            items=request.items
        )

    @staticmethod
    def list_orders(db: Session, user):
        if user["role"] == "admin":
            return OrderRepository.list_all(db)

        return OrderRepository.list_by_department(
            db=db,
            department_id=user["department_id"]
        )

    @staticmethod
    def update_order_status(db: Session, order_id, status: OrderStatus, user):
        if user["role"] != "admin":
            raise ValueError("Only admin can update order status")

        order = OrderRepository.get_by_id(db, order_id)
        if not order:
            raise ValueError("Order not found")

        return OrderRepository.update_status(db, order, status)
