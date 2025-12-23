from sqlalchemy.orm import Session

from app.user_repository import UserRepository
from app.utils import verify_password, create_access_token, create_refresh_token


class AuthService:

    @staticmethod
    def register(db: Session, request):
        user = UserRepository.create_user(
            db=db,
            email=request.email,
            password=request.password,
            name=request.name,
            role=request.role,
            department_id=request.department_id
        )

        return user

    @staticmethod
    def login(db: Session, request):
        user = UserRepository.get_by_email(db, request.email)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(request.password, user.password_hash):
            raise ValueError("Invalid credentials")

        access_token = create_access_token({
            "sub": str(user.id),
            "role": user.role.value,
            "department_id": str(user.department_id)
        })

        refresh_token = create_refresh_token({
            "sub": str(user.id)
        })

        user.last_login = user.last_login = None
        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
