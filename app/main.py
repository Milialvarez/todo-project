from fastapi import FastAPI
from app.api.v1.endpoints import auth, reminders, tasks, test, users
from fastapi.middleware.cors import CORSMiddleware

from app.core.scheduler import start_scheduler      


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    start_scheduler()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
app.include_router(test.router)
