from fastapi import FastAPI
from app.api.v1.endpoints import tasks

app = FastAPI()

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
