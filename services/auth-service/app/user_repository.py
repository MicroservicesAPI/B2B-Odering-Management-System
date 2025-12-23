from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.utils import hash_password


class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(
        db: Session,
        email: str,
        password: str,
        name: str,
        role,
        department_id
    ) -> User:
        user = User(
            email=email,
            name=name,
            password_hash=hash_password(password),
            role=role,
            department_id=department_id
        )

        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("User with this email already exists")

        db.refresh(user)
        return user
