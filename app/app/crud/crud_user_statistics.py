from typing import List

from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import coalesce

from app.models.assignment import ModelAssignment
from app.models.task import ModelTask
from app.models.user import ModelUser
from app.schemas.task import TaskStatus
from app.schemas.user import UserId


def assigned_task_counts(db: Session, user_ids: List[UserId], status: TaskStatus):
    """
    ユーザーにアサインされているタスクの件数を集計する。
    タスクの件数は優先度ごとに分類される。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    user_ids : List[UserId]
        検索対象にするユーザー群。
    status : TaskStatus
        検索するステータス。
    """
    return (
        db.query(
            ModelAssignment.user_id,
            ModelTask.priority,
            func.count(ModelTask.id).label("task_count"),
        )
        .join(ModelTask)
        .filter(ModelAssignment.user_id.in_([user_id.id for user_id in user_ids]))
        .filter(ModelTask.status == status)
        .group_by(ModelAssignment.user_id, ModelTask.priority)
        .order_by(ModelAssignment.user_id, desc(ModelTask.priority))
        .all()
    )


def status_task_counts(db: Session, status: TaskStatus, limit: int, offset: int):
    """
    ユーザーにアサインされたタスクのうち、指定されたステータスであるものの件数を計算する。
    1. アサインされたタスクが多いもの
    2. ユーザーID が小さいもの
    の順に検索される。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    status : TaskStatus
        検索するステータス。
    limit : int
        １回の検索で取得する件数の上限。
    offset : int
        先頭を読み飛ばす件数。

    returns
    -------
    any
        「ユーザーIDと、アサインされたタスクの数の組」のリスト。
    """
    subquery = (
        db.query(ModelAssignment.user_id, func.count(ModelTask.id).label("task_count"))
        .join(ModelTask)
        .filter(ModelTask.status == status)
        .group_by(ModelAssignment.user_id)
        .subquery()
    )
    return (
        db.query(ModelUser.id, coalesce(subquery.c.task_count, 0).label("task_count"))
        .outerjoin(subquery)
        .order_by(desc(coalesce(subquery.c.task_count, 0)), ModelUser.id)
        .limit(limit)
        .offset(offset)
        .all()
    )
