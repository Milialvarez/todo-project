from fastapi import FastAPI, Request
from app.api.v1.endpoints import admin, auth, reminders, tasks, test, users
from fastapi.middleware.cors import CORSMiddleware
from app.core.handlers import (
    app_exception_handler,
    not_found_handler,
    permission_denied_handler,
    invalid_token_handler,
)
from app.core.exceptions import (
    AppException,
    TaskNotFoundError,
    ReminderNotFoundError,
    UserNotFoundError,
    PermissionDeniedError,
    InvalidTokenError,
)
from app.core.scheduler import start_scheduler
from app.middlewares.auth_context import auth_context_middleware
from app.middlewares.error_logging import error_logging_middleware
from app.middlewares.logging import logging_middleware   

app = FastAPI()

# CORS middleware
# Allows the Next.js frontend to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generic business exception handler
app.add_exception_handler(AppException, app_exception_handler)

# Not found domain exceptions
app.add_exception_handler(TaskNotFoundError, not_found_handler)
app.add_exception_handler(ReminderNotFoundError, not_found_handler)
app.add_exception_handler(UserNotFoundError, not_found_handler)

# Authentication / authorization exceptions
app.add_exception_handler(PermissionDeniedError, permission_denied_handler)
app.add_exception_handler(InvalidTokenError, invalid_token_handler)

# Logging, auth & error middlewares
@app.middleware("http")
async def auth_context(request: Request, call_next):
    return await auth_context_middleware(request, call_next)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    return await logging_middleware(request, call_next)

@app.middleware("http")
async def log_errors(request: Request, call_next):
    return await error_logging_middleware(request, call_next)

# Startup event
# Used to initialize the scheduler that sends reminder emails.
@app.on_event("startup")
def startup_event():
    start_scheduler()

# API routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
app.include_router(test.router)
app.include_router(admin.router)
