from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreateReq


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_mail(db: Session, mail: str):
    return db.query(User).filter(User.mail == mail).first()


def get_users(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, req: UserCreateReq):
    db_user = User(name=req.name, mail=req.mail)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user