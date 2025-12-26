from app.schemas import UserRole
from app.user_repository import UserRepository


def test_create_and_get_user(db):
    user = UserRepository.create_user(
        db=db,
        email="test@example.com",
        password="password123",
        name="Test User",
        role=UserRole.STAFF,
        department_id="11111111-1111-1111-1111-111111111111"
    )

    fetched = UserRepository.get_by_email(db, "test@example.com")

    assert fetched is not None
    assert fetched.email == user.email
    assert fetched.name == "Test User"
