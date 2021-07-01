from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas.user import UserCreate


def test_create_user(sample_db: Session) -> None:
    name = "user7"
    mail = "user7@example.com"
    user = UserCreate(name=name, mail=mail)
    user_model = crud_user.create(sample_db, user=user)
    assert user_model.name == name
    assert user_model.mail == mail


def test_user_find(sample_db: Session) -> None:
    users = crud_user.all(db=sample_db, limit=100, offset=0)
    assert len(users) == 6
