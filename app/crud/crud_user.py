from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def find(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def find_by_mail(db: Session, mail: str):
    return db.query(User).filter(User.mail == mail).first()


def all(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()


def create(db: Session, user: UserCreate):
    db_user = User(name=user.name, mail=user.mail)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete(db: Session, user_id: int):
    db_user = db.query(User).get(user_id)
    db.delete(db_user)
    db.commit()
    return db_user
