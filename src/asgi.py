from .repository.config import Base, engine
from .todo.routes import todos
from .main import create_app

Base.metadata.create_all(bind=engine)
app = create_app()
app.include_router(todos)
