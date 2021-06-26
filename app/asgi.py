from app.main import create_app
from app.todo.assignments import assignments
from app.todo.tasks import tasks
from app.todo.users import users

app = create_app()
app.include_router(users)
app.include_router(tasks)
app.include_router(assignments)
