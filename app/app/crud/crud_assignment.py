from sqlalchemy.orm import Session

from app.models.assignment import ModelAssignment
from app.schemas.assignment import AssignmentCreate
from app.schemas.task import TaskId
from app.schemas.user import UserId


def find(db: Session, user_id: UserId, task_id: TaskId):
    """
    assignments テーブルから１件エントリを取得する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    user_id: UserId
        検索するユーザーID。
    task_id: TaskId
        検索するタスクID。

    Returns
    -------
    ModelAssignment | None
        検索されたエントリ。
    """
    return (
        db.query(ModelAssignment)
        .filter(ModelAssignment.user_id == user_id.id)
        .filter(ModelAssignment.task_id == task_id.id)
        .first()
    )


def create(db: Session, assignment: AssignmentCreate):
    """
    assignments テーブルに１件エントリを生成する。

    Parameters
    ----------
    db : sqlalchemy.orm.Session
        接続するデータベース。
    assignment: AssignmentCreate
        生成するアサインの情報。
        id は SERIAL によって採番されるので、id の情報は含まない。

    Returns
    -------
    ModelAssignment
        生成されたエントリ。
        SERIAL によって採番された id の情報を含む。
    """
    db_assignment = ModelAssignment(user_id=assignment.user_id, task_id=assignment.task_id)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
