from fastapi import FastAPI
from app.api.v1.endpoints import auth, tasks, users
from fastapi.middleware.cors import CORSMiddleware      

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

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
