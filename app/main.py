from fastapi import FastAPI
from app.api.v1.endpoints import auth, reminders, tasks, users
from fastapi.middleware.cors import CORSMiddleware      
from app.db.session import engine
from app.db.models.models import Base


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
