from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.core.exceptions import (
    PermissionDeniedError,
    InvalidTokenError,
)

# Generic handler for business/domain exceptions.
# This handler catches any exception that inherits from AppException and returns a controlled 400 response.
# It avoids leaking stack traces to the frontend and keeps error responses consistent across the API.
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
        },
    )

# Handler for "not found" domain errors.
# Used when a requested resource (task, reminder, user) does not exist in the system.
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
        },
    )

# Handler for authorization/permission errors.
# Used when a user is authenticated but does not have enough privileges to perform an action.
async def permission_denied_handler(request: Request, exc: PermissionDeniedError):
    return JSONResponse(
        status_code=403,
        content={
            "error": "Forbidden",
            "message": str(exc),
        },
    )

# Handler for authentication/token-related errors.
# Used when access or refresh tokens are invalid, expired, or malformed.
async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=401,
        content={
            "error": "Unauthorized",
            "message": str(exc),
        },
    )
