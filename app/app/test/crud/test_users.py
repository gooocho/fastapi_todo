from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas.user import UserCreate, UserId, UserUpdate

class TestUsers:
    def test_user_find(self, sample_db: Session) -> None:
        user1 = crud_user.find(db=sample_db, user_id=UserId(id=1))
        assert user1.id == 1


    def test_user_find_by_id(self, sample_db: Session) -> None:
        user1 = crud_user.find_by_id(db=sample_db, user_id=UserId(id=1))
        assert user1.id == 1


    def find_by_mail(self, sample_db: Session) -> None:
        user1 = crud_user.find_by_mail(db=sample_db, mail="user1@example.com")
        assert user1.id == 1


    def test_user_all(self, sample_db: Session) -> None:
        users = crud_user.all(db=sample_db, limit=100, offset=0)
        assert len(users) == 6


    def test_user_all_id(self, sample_db: Session) -> None:
        user_ids = crud_user.all_id(db=sample_db, limit=100, offset=0)
        assert len(user_ids) == 6
        assert user_ids[0].id == 1


    def test_user_create(self, sample_db: Session) -> None:
        name = "user7"
        mail = "user7@example.com"
        user = UserCreate(name=name, mail=mail)
        user_model = crud_user.create(sample_db, user=user)
        assert user_model.name == name
        assert user_model.mail == mail
        assert list(sample_db.execute("SELECT COUNT(*) FROM users;"))[0][0] == 7


    def test_user_update(self, sample_db: Session) -> None:
        name = "user1_updated"
        mail = "user1_updated@example.com"
        user = UserUpdate(id=1, name=name, mail=mail)
        user_model = crud_user.update(sample_db, user=user)
        assert user_model.name == name
        assert user_model.mail == mail


    def test_user_delete(self, sample_db: Session) -> None:
        name = "user1"
        mail = "user1@example.com"
        user_model = crud_user.delete(sample_db, user_id=UserId(id=1))
        assert user_model.name == name
        assert user_model.mail == mail
        assert list(sample_db.execute("SELECT COUNT(*) FROM users;"))[0][0] == 5
