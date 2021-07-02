from sqlalchemy.orm import Session

from app.crud import crud_assignment
from app.schemas.assignment import AssignmentCreate
from app.schemas.task import TaskId
from app.schemas.user import UserId


def test_assignment_find(sample_db: Session) -> None:
    assignment1 = crud_assignment.find(
        db=sample_db, user_id=UserId(id=2), task_id=TaskId(id=1)
    )
    assert assignment1.user_id == 2
    assert assignment1.task_id == 1


def test_assignment_create(sample_db: Session) -> None:
    assignments_count = list(sample_db.execute("SELECT COUNT(*) FROM assignments;"))[0][
        0
    ]
    user_id = 1
    task_id = 1

    assignment = AssignmentCreate(user_id=user_id, task_id=task_id)
    assignment_model = crud_assignment.create(sample_db, assignment=assignment)

    assert (
        list(sample_db.execute("SELECT COUNT(*) FROM assignments;"))[0][0]
        == assignments_count + 1
    )
    assert assignment_model.user_id == user_id
    assert assignment_model.task_id == task_id
