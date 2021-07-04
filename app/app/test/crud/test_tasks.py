import pytest

from sqlalchemy.orm import Session

from app.crud import crud_task
from app.schemas.task import TaskCreate, TaskId, TaskPriority, TaskStatus, TaskUpdate
from app.schemas.user import UserId


class TestTasks:
    def test_task_find(self, test_db: Session) -> None:
        task1 = crud_task.find(db=test_db, task_id=TaskId(id=1))
        assert task1.id == 1

    def test_task_all(self, test_db: Session) -> None:
        tasks = crud_task.all(db=test_db, limit=100, offset=0)
        assert len(tasks) == 70

    def test_task_create(self, test_db: Session) -> None:
        task_count = list(test_db.execute("SELECT COUNT(*) FROM tasks;"))[0][0]
        title = "task61 title"
        description = "task61 description"
        priority = TaskPriority.NORMAL
        status = TaskStatus.NEW

        task = TaskCreate(
            title=title, description=description, priority=priority, status=status
        )
        task_model = crud_task.create(test_db, task=task)

        assert (
            list(test_db.execute("SELECT COUNT(*) FROM tasks;"))[0][0] == task_count + 1
        )
        assert task_model.title == title
        assert task_model.description == description
        assert task_model.priority == priority
        assert task_model.status == status

    def test_task_update(self, test_db: Session) -> None:
        title = "task1 title updated"
        description = "task1 description updated"
        priority = TaskPriority.HIGH
        status = TaskStatus.RESOLVED
        task = TaskUpdate(
            id=1, title=title, description=description, priority=priority, status=status
        )
        task_model = crud_task.update(test_db, task=task)
        assert task_model.title == title
        assert task_model.description == description
        assert task_model.priority == priority
        assert task_model.status == status

    @pytest.mark.parametrize(
        "statuses, expect",
        [
            ([TaskStatus.NEW], 30),
            ([TaskStatus.IN_PROGRESS], 20),
            ([TaskStatus.RESOLVED], 20),
            ([TaskStatus.NEW, TaskStatus.IN_PROGRESS], 50),
            ([TaskStatus.NEW, TaskStatus.RESOLVED], 50),
            ([TaskStatus.IN_PROGRESS, TaskStatus.RESOLVED], 40),
            ([TaskStatus.NEW, TaskStatus.IN_PROGRESS, TaskStatus.RESOLVED], 70),
        ],
    )
    def test_task_filterd_by_status(self, statuses, expect, test_db: Session) -> None:
        tasks = crud_task.filterd_by_status(
            test_db,
            statuses=statuses,
            limit=100,
            offset=0,
        )
        assert len(tasks) == expect

    @pytest.mark.parametrize(
        "statuses, expect",
        [
            ([TaskStatus.NEW], 10),
            ([TaskStatus.IN_PROGRESS], 0),
            ([TaskStatus.RESOLVED], 0),
        ],
    )
    def test_task_not_assigned(self, statuses, expect, test_db: Session) -> None:
        tasks = crud_task.not_assigned(
            test_db, statuses=statuses, limit=100, offset=0
        )
        assert len(tasks) == expect

    @pytest.mark.parametrize(
        "id, statuses, expect",
        [
            (1, [TaskStatus.NEW], 15),
            (1, [TaskStatus.IN_PROGRESS], 0),
            (1, [TaskStatus.RESOLVED], 0),
            (2, [TaskStatus.NEW], 0),
            (2, [TaskStatus.IN_PROGRESS], 15),
            (2, [TaskStatus.RESOLVED], 0),
            (3, [TaskStatus.NEW], 0),
            (3, [TaskStatus.IN_PROGRESS], 0),
            (3, [TaskStatus.RESOLVED], 15),
            (4, [TaskStatus.NEW], 20),
            (4, [TaskStatus.IN_PROGRESS], 20),
            (4, [TaskStatus.RESOLVED], 20),
            (4, [TaskStatus.NEW, TaskStatus.IN_PROGRESS], 40),
            (4, [TaskStatus.NEW, TaskStatus.RESOLVED], 40),
            (4, [TaskStatus.IN_PROGRESS, TaskStatus.RESOLVED], 40),
            (4, [TaskStatus.NEW, TaskStatus.IN_PROGRESS, TaskStatus.RESOLVED], 60),
        ],
    )
    def test_task_with_user_filtered_by_statuses(
        self, id, statuses, expect, test_db: Session
    ) -> None:
        tasks = crud_task.with_user_filtered_by_statuses(
            test_db,
            user_id=UserId(id=id),
            statuses=statuses,
            limit=100,
            offset=0,
        )
        assert len(tasks) == expect
