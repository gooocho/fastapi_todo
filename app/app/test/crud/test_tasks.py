from sqlalchemy.orm import Session

from app.crud import crud_task
from app.schemas.task import TaskCreate, TaskId, TaskPriority, TaskStatus, TaskUpdate
from app.schemas.user import UserId


def test_task_find(sample_db: Session) -> None:
    task1 = crud_task.find(db=sample_db, task_id=TaskId(id=1))
    assert task1.id == 1


def test_task_all(sample_db: Session) -> None:
    tasks = crud_task.all(db=sample_db, limit=100, offset=0)
    assert len(tasks) == 6


def test_task_create(sample_db: Session) -> None:
    task_count = list(sample_db.execute("SELECT COUNT(*) FROM tasks;"))[0][0]
    title = "task7 title"
    description = "task7 description"
    priority = TaskPriority.NORMAL
    status = TaskStatus.NEW

    task = TaskCreate(
        title=title, description=description, priority=priority, status=status
    )
    task_model = crud_task.create(sample_db, task=task)

    assert (
        list(sample_db.execute("SELECT COUNT(*) FROM tasks;"))[0][0] == task_count + 1
    )
    assert task_model.title == title
    assert task_model.description == description
    assert task_model.priority == priority
    assert task_model.status == status


def test_task_update(sample_db: Session) -> None:
    title = "task7 title updated"
    description = "task7 description updated"
    priority = TaskPriority.HIGH
    status = TaskStatus.RESOLVED
    task = TaskUpdate(
        id=1, title=title, description=description, priority=priority, status=status
    )
    task_model = crud_task.update(sample_db, task=task)
    assert task_model.title == title
    assert task_model.description == description
    assert task_model.priority == priority
    assert task_model.status == status


def test_task_filterd_by_status(sample_db: Session) -> None:
    tasks = crud_task.filterd_by_status(
        sample_db,
        statuses=[TaskStatus.NEW, TaskStatus.IN_PROGRESS],
        limit=100,
        offset=0,
    )
    assert len(tasks) == 6


def test_task_not_assigned(sample_db: Session) -> None:
    tasks = crud_task.not_assigned(
        sample_db, statuses=[TaskStatus.NEW], limit=100, offset=0
    )
    assert len(tasks) == 0


def test_task_not_resolved(sample_db: Session) -> None:
    tasks = crud_task.not_resolved(
        sample_db, user_id=UserId(id=1), statuses=[TaskStatus.NEW], limit=100, offset=0
    )
    assert len(tasks) == 0
