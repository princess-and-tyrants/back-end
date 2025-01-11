from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt

# JWT Secret Key
secret_key = "gTA8B7V5W24-7jcn1IFoY0FHsBqgQ_Z6TWYD-J4Cyb4="

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_routes=None, excluded_prefixes=None):
        super().__init__(app)
        self.allowed_routes = allowed_routes or []  # 명시적으로 허용된 경로
        self.excluded_prefixes = excluded_prefixes or []  # 제외할 경로 접두사

    async def dispatch(self, request: Request, call_next):
         # 요청 경로가 제외할 접두사로 시작하면 검증하지 않음
        for prefix in self.excluded_prefixes:
            if request.url.path.startswith(prefix):
                return await call_next(request)

        if "Authorization" not in request.headers:
            return JSONResponse(status_code=499, content={"detail": "Authorization header missing."})

        auth_header = request.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=499, content={"detail": "Invalid Authorization header format."})

        token = auth_header.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            request.state.user = decoded_token  # Attach user information to the request state
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=499, content={"detail": "Token has expired."})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=499, content={"detail": "Invalid token."})

        response = await call_next(request)
        return response

class BlockUndefinedRoutesMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_routes):
        super().__init__(app)
        self.allowed_routes = allowed_routes

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.allowed_routes:
            return JSONResponse(status_code=404, content={"detail": "Route not found."})
        return await call_next(request)