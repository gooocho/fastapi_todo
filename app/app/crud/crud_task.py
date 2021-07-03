from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.assignment import ModelAssignment
from app.models.task import ModelTask
from app.schemas.task import TaskCreate, TaskId, TaskStatus, TaskUpdate
from app.schemas.user import UserId


def find(db: Session, task_id: TaskId):
    """
    tasks テーブルから１件エントリを取得する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    task_id : TaskId
        検索するタスクID。

    Returns
    -------
    ModelTask | None
        検索されたエントリ。
    """
    return db.query(ModelTask).filter(ModelTask.id == task_id.id).first()


def all(db: Session, limit: int, offset: int):
    """
    tasks テーブルから条件を指定せずエントリを取得する。
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
    List[ModelTask]
        検索されたエントリ。
    """
    return db.query(ModelTask).order_by(ModelTask.id).limit(limit).offset(offset).all()


def create(db: Session, task: TaskCreate):
    """
    tasks テーブルに１件エントリを生成する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    task : TaskCreate
        生成するタスクの情報。
        id は SERIAL によって採番されるので、id の情報は含まない。

    Returns
    -------
    ModelTask
        生成されたエントリ。
        SERIAL によって採番された id の情報を含む。
    """
    db_task = ModelTask(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update(db: Session, task: TaskUpdate):
    """
    tasks テーブルのエントリを１件更新する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    task : TaskUpdate
        更新するタスク。

    Returns
    -------
    ModelTask | None
        更新されたエントリ。
    """
    db_task = db.query(ModelTask).filter(ModelTask.id == task.id)
    compacted = {k: v for (k, v) in task.dict().items() if v is not None and k != "id"}
    if len(compacted):
        db_task.update(compacted)
        db.commit()
    return db_task.first()


def filterd_by_status(db: Session, statuses: List[TaskStatus], limit: int, offset: int):
    """
    tasks テーブルのエントリのうち、指定されたステータスであるものを検索する。
    1. ステータスが進んでいるもの（（進んでいる）完了 > 作業中 > 未着手（進んでいない））
    2. 優先度が大きいもの
    3. ID が小さいもの
    の順に検索される。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    statuses : List[TaskStatus]
        検索するステータス。
    limit : int
        １回の検索で取得する件数の上限。
    offset : int
        先頭を読み飛ばす件数。

    Returns
    -------
    List[ModelTask]
        検索されたエントリ。
    """
    return (
        db.query(ModelTask)
        .filter(ModelTask.status.in_(statuses))
        .order_by(desc(ModelTask.status), desc(ModelTask.priority), ModelTask.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def not_assigned(db: Session, statuses: List[TaskStatus], limit: int, offset: int):
    """
    tasks テーブルのエントリのうち、ユーザーに全くアサインされていないものを検索する。
    1. 優先度が大きいもの
    2. ID が小さいもの
    の順に検索される。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    statuses : List[TaskStatus]
        検索するステータス。
    limit : int
        １回の検索で取得する件数の上限。
    offset : int
        先頭を読み飛ばす件数。

    Returns
    -------
    List[ModelTask]
        検索されたエントリ。
    """
    subquery = (
        ~db.query(ModelAssignment.task_id)
        .filter(ModelAssignment.task_id == ModelTask.id)
        .exists()
    )
    return (
        db.query(ModelTask)
        .filter(ModelTask.status.in_(statuses))
        .filter(subquery)
        .order_by(desc(ModelTask.priority), ModelTask.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def with_user_filtered_by_statuses(
    db: Session, user_id: UserId, statuses: List[TaskStatus], limit: int, offset: int
):
    """
    tasks テーブルのエントリのうち、指定したユーザーにアサインされている、
    指定されたステータスであるものを検索する。
    1. ステータスが進んでいるもの（（進んでいる）完了 > 作業中 > 未着手（進んでいない））
    2. 優先度が大きいもの
    3. ID が小さいもの
    の順に検索される。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    user_id : UserId
        検索するユーザー。
    statuses : List[TaskStatus]
        検索するステータス。
    limit : int
        １回の検索で取得する件数の上限。
    offset : int
        先頭を読み飛ばす件数。

    Returns
    -------
    List[ModelTask]
        検索されたエントリ。
    """
    return (
        db.query(ModelTask)
        .join(ModelAssignment)
        .filter(ModelTask.status.in_(statuses))
        .filter(ModelAssignment.user_id == user_id.id)
        .order_by(desc(ModelTask.status), desc(ModelTask.priority), ModelTask.id)
        .limit(limit)
        .offset(offset)
        .all()
    )
