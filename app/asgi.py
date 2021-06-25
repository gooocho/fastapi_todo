from app.todo.users import users
from app.todo.tasks import tasks
from app.todo.assignments import assignments
from .main import create_app

app = create_app()
app.include_router(users)
app.include_router(tasks)
app.include_router(assignments)
