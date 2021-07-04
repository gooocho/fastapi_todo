import pytest

from sqlalchemy.orm import Session

from app.crud import crud_user_statistics
from app.schemas.task import TaskStatus
from app.schemas.user import UserId


class TestUserStatistics:
    def test_assigned_task_counts(self, test_db: Session) -> None:
        assigned_task_counts = crud_user_statistics.assigned_task_counts(
            db=test_db,
            user_ids=[UserId(id=1), UserId(id=2), UserId(id=3), UserId(id=4)],
            status=TaskStatus.NEW,
        )
        assert len(assigned_task_counts) == 10
        assert assigned_task_counts == [
            (1, 5, 5),
            (1, 4, 4),
            (1, 3, 3),
            (1, 2, 2),
            (1, 1, 1),
            (4, 5, 6),
            (4, 4, 5),
            (4, 3, 4),
            (4, 2, 3),
            (4, 1, 2),
        ]

    @pytest.mark.parametrize(
        "status, status_task_counts_expect",
        [
            (TaskStatus.NEW, [(4, 20), (1, 15), (2, 0), (3, 0), (5, 0), (6, 0)]),
            (
                TaskStatus.IN_PROGRESS,
                [(4, 20), (2, 15), (1, 0), (3, 0), (5, 0), (6, 0)],
            ),
            (TaskStatus.RESOLVED, [(4, 20), (3, 15), (1, 0), (2, 0), (5, 0), (6, 0)]),
        ],
    )
    def test_status_task_counts(
        self, status, status_task_counts_expect, test_db: Session
    ):
        status_task_counts = crud_user_statistics.status_task_counts(
            db=test_db, status=status, limit=100, offset=0
        )
        assert len(status_task_counts) == 6
        assert status_task_counts == status_task_counts_expect
