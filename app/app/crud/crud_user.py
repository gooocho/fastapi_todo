from sqlalchemy.orm import Session

from app.models.user import ModelUser
from app.schemas.user import UserCreate, UserId, UserUpdate


def find(db: Session, user_id: UserId):
    """
    id で検索して１件ユーザーを取得する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    user_id : UserId
        検索するユーザーID。

    Returns
    -------
    ModelUser | None
        検索されたユーザー。
    """
    return db.query(ModelUser).filter(ModelUser.id == user_id.id).first()


def find_by_mail(db: Session, mail: str):
    """
    mail で検索して１件ユーザーを取得する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    mail : str
        検索するメールアドレス。
        メールアドレスはユーザー全体でユニーク。

    Returns
    -------
    ModelUser | None
        検索されたユーザー。
    """
    return db.query(ModelUser).filter(ModelUser.mail == mail).first()


def all(db: Session, limit: int, offset: int):
    """
    条件を指定せずユーザーを検索する。
    ID の小さいものから順に検索される。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    limit : int
        １回の検索で取得する件数の上限。
    offset : int
        先頭を読み飛ばす件数。

    Returns
    -------
    List[ModelUser]
        検索されたユーザー。
    """
    return db.query(ModelUser).order_by(ModelUser.id).limit(limit).offset(offset).all()


def all_id(db: Session, limit: int, offset: int):
    """
    条件を指定せずユーザーを検索する。
    ユーザーの情報すべては含まず id の情報のみが取得できる。
    ID の小さいものから順に検索される。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    limit : int
        １回の検索で取得する件数の上限。
    offset : int
        先頭を読み飛ばす件数。

    Returns
    -------
    List[int]
        検索されたユーザーの id のリスト。
    """
    return (
        db.query(ModelUser.id).order_by(ModelUser.id).limit(limit).offset(offset).all()
    )


def create(db: Session, user: UserCreate):
    """
    ユーザーを１件生成する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    user : UserCreate
        生成するユーザーの情報。
        id は SERIAL によって採番されるので、id の情報は含まない。

    Returns
    -------
    ModelUser
        生成されたユーザー。
        SERIAL によって採番された id の情報を含む。
    """
    db_user = ModelUser(name=user.name, mail=user.mail)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(db: Session, user: UserUpdate):
    """
    ユーザーを１件更新する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    user : UserUpdate
        更新するユーザー。

    Returns
    -------
    ModelUser | None
        更新されたユーザー。
    """
    db_user = db.query(ModelUser).filter(ModelUser.id == user.id)
    compacted = {k: v for (k, v) in user.dict().items() if v is not None and k != "id"}
    if len(compacted):
        db_user.update(compacted)
        db.commit()
    return db_user.first()


def delete(db: Session, user_id: UserId):
    """
    ユーザーを１件削除する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    user_id : UserId
        削除するユーザーID。

    Returns
    -------
    ModelUser | None
        削除されたユーザー。
    """
    db_user = db.query(ModelUser).get(user_id.id)
    db.delete(db_user)
    db.commit()
    return db_user
