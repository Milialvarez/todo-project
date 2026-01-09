import logging
from fastapi import Request

logger = logging.getLogger("app")

async def error_logging_middleware(request: Request, call_next):
    """
    Logs requests that result in client or server errors (status >= 400).
    """

    response = await call_next(request)

    if response.status_code >= 500:
        logger.error(
            "Server error %s %s - %s",
            request.method,
            request.url.path,
            response.status_code,
        )

    elif response.status_code >= 400:
        logger.warning(
            "Client error %s %s - %s",
            request.method,
            request.url.path,
            response.status_code,
        )

    return response
