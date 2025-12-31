from sqlalchemy.orm import Session

from app.db.models import Order, OrderItem, OrderStatus


class OrderRepository:

    @staticmethod
    def create_order(
        db: Session,
        user_id,
        department_id,
        description,
        items
    ) -> Order:

        order = Order(
            user_id=user_id,
            department_id=department_id,
            description=description,
            status=OrderStatus.PENDING
        )

        db.add(order)
        db.flush()  # get order.id before commit

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_name=item.product_name,
                quantity=item.quantity
            )
            db.add(order_item)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_by_id(db: Session, order_id) -> Order | None:
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def list_by_department(db: Session, department_id: int):
        return (
            db.query(Order)
            .filter(Order.department_id == department_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    @staticmethod
    def list_by_user(db: Session, user_id):
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    @staticmethod
    def list_all(db: Session):
        return db.query(Order).order_by(Order.created_at.desc()).all()

    @staticmethod
    def update_status(db: Session, order: Order, status: OrderStatus):
        order.status = status
        db.commit()
        db.refresh(order)
        return order
