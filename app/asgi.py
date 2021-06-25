from app.todo.users import users
from app.todo.tasks import tasks
from .main import create_app

app = create_app()
app.include_router(users)
app.include_router(tasks)
