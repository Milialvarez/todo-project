import time
import logging
from fastapi import Request

logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)

async def logging_middleware(request: Request, call_next):
    """
    Middleware that logs basic information about each request:
    - HTTP method
    - Path
    - Response status code
    - Time spent processing the request
    """

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    process_time_ms = process_time * 1000

    # Add response time header
    response.headers["X-Response-Time"] = f"{process_time_ms:.2f}ms"

    # Log request info
    logger.info(
        "%s %s - %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        process_time_ms,
    )

    return response
