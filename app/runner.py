import uvicorn
from fastapi import FastAPI

from app.todo.assignments import assignments
from app.todo.tasks import tasks
from app.todo.user_statistics import user_statistics
from app.todo.users import users

app = FastAPI()

app.include_router(users)
app.include_router(tasks)
app.include_router(assignments)
app.include_router(user_statistics)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
