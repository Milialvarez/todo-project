from fastapi import Request

async def auth_context_middleware(request: Request, call_next):
    """
    Extracts authentication context from the Authorization header
    and stores it in request.state for later use.
    """

    request.state.user_id = None
    request.state.token = None

    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        request.state.token = token

    response = await call_next(request)
    return response
