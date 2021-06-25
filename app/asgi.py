from .todo.routes import todos
from .main import create_app

app = create_app()
app.include_router(todos)
