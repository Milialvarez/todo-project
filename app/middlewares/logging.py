import time
import logging
from fastapi import Request

# Basic logger config
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

    # Let the request continue through the app
    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        "%s %s - %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        process_time * 1000,
    )

    return response
