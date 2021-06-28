from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserId, UserUpdate


def find(db: Session, user_id: UserId):
    return db.query(User).filter(User.id == user_id.id).first()


def find_by_id(db: Session, user_id: UserId):
    return db.query(User).filter(User.id == user_id.id).order_by(User.id).all()


def find_by_mail(db: Session, mail: str):
    return db.query(User).filter(User.mail == mail).first()


def all(db: Session, limit: int, offset: int):
    return db.query(User).order_by(User.id).limit(limit).offset(offset).all()


def all_id(db: Session, limit: int, offset: int):
    return db.query(User.id).order_by(User.id).limit(limit).offset(offset).all()


def create(db: Session, user: UserCreate):
    db_user = User(name=user.name, mail=user.mail)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(db: Session, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user.id)
    compacted = {k: v for (k, v) in user.dict().items() if v is not None and k != "id"}
    if len(compacted):
        db_user.update(compacted)
        db.commit()
    return db_user.first()


def delete(db: Session, user_id: UserId):
    db_user = db.query(User).get(user_id.id)
    db.delete(db_user)
    db.commit()
    return db_user
