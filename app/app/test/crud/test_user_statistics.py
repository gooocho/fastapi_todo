from typing import List

from sqlalchemy.orm import Session

from app.crud import crud_user_statistics
from app.schemas.task import TaskStatus
from app.schemas.user import UserId


class TestUserStatistics:
    def test_assigned_task_counts(self, test_db: Session) -> None:
        assigned_task_counts = crud_user_statistics.assigned_task_counts(
            db=test_db, user_ids=[UserId(id=2), UserId(id=3)], status=TaskStatus.NEW
        )
        assert len(assigned_task_counts) == 2
        assert assigned_task_counts == [(2, 1, 3), (3, 1, 1)]

    def test_status_task_counts(self, test_db: Session):
        status_task_counts = crud_user_statistics.status_task_counts(
            db=test_db, status=TaskStatus.NEW, limit=100, offset=0
        )
        assert len(status_task_counts) == 6
        assert status_task_counts == [(4, 6), (2, 3), (5, 3), (6, 2), (3, 1), (1, 0)]
