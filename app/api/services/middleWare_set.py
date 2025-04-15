from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class MiddlewareNoCache(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if 'cache-control' not in response.headers:
            response.headers['Cache-Control'] = "no-store, no-cache, must-revalidate, max-age=0"
        if 'expires' not in response.headers:
            response.headers['Expires'] = '0'
        if 'pragma' not in response.headers:
            response.headers['Pragma'] = 'no-cache'

        return response