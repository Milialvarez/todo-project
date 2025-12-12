from fastapi import FastAPI
from app.api.v1.endpoints import auth, tasks, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
