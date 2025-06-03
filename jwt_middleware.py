from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

# JWT Secret Key
secret_key = "gTA8B7V5W24-7jcn1IFoY0FHsBqgQ_Z6TWYD-J4Cyb4="

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_routes=None, excluded_prefixes=None):
        super().__init__(app)
        self.allowed_routes = allowed_routes or []  # 명시적으로 허용된 경로
        self.excluded_prefixes = excluded_prefixes or []  # 제외할 경로 접두사

    async def dispatch(self, request: Request, call_next):
        # 디버깅 로그 추가
        print(f"[JWTMiddleware] Request Path: {request.url.path}")
        print(f"[JWTMiddleware] Allowed Routes: {self.allowed_routes}")
        print(f"[JWTMiddleware] Excluded Prefixes: {self.excluded_prefixes}")

        # 요청 경로가 제외할 접두사로 시작하면 검증하지 않음
        for prefix in self.excluded_prefixes:
            if request.url.path.startswith(prefix):
                print(f"[JWTMiddleware] Path '{request.url.path}' excluded.")
                return await call_next(request)

        # Authorization 헤더 확인
        if "Authorization" not in request.headers:
            print("[JWTMiddleware] Authorization header missing.")
            return JSONResponse(status_code=499, content={"detail": "Authorization header missing."})

        auth_header = request.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            print("[JWTMiddleware] Invalid Authorization header format.")
            return JSONResponse(status_code=499, content={"detail": "Invalid Authorization header format."})

        # JWT 토큰 검증
        token = auth_header.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            request.state.user = decoded_token  # Attach user information to the request state
            print("[JWTMiddleware] Token decoded successfully.")
        except jwt.ExpiredSignatureError:
            print("[JWTMiddleware] Token has expired.")
            return JSONResponse(status_code=499, content={"detail": "Token has expired."})
        except jwt.InvalidTokenError:
            print("[JWTMiddleware] Invalid token.")
            return JSONResponse(status_code=499, content={"detail": "Invalid token."})

        # 다음 미들웨어로 이동
        response = await call_next(request)
        return response


class BlockUndefinedRoutesMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_routes, excluded_prefixes=None):
        super().__init__(app)
        self.allowed_routes = allowed_routes  # 명시적으로 허용된 경로
        self.excluded_prefixes = excluded_prefixes or []  # 제외할 접두사

    async def dispatch(self, request: Request, call_next):
        # 디버깅 로그 추가
        print(f"[BlockUndefinedRoutesMiddleware] Request Path: {request.url.path}")
        print(f"[BlockUndefinedRoutesMiddleware] Allowed Routes: {self.allowed_routes}")
        print(f"[BlockUndefinedRoutesMiddleware] Excluded Prefixes: {self.excluded_prefixes}")

        # 제외 경로 확인
        for prefix in self.excluded_prefixes:
            if request.url.path.startswith(prefix):
                print(f"[BlockUndefinedRoutesMiddleware] Path '{request.url.path}' excluded.")
                return await call_next(request)

        # 허용된 경로 확인
        allowed = False
        for route in self.allowed_routes:
            if request.url.path == route or request.url.path.startswith(route + "/"):
                allowed = True
                break
        if not allowed:
            print(f"[BlockUndefinedRoutesMiddleware] Path '{request.url.path}' not allowed.")
            return JSONResponse(status_code=404, content={"detail": f"Route not found: {request.url.path}"})
        
        # if request.url.path not in self.allowed_routes:
        #     print(f"[BlockUndefinedRoutesMiddleware] Path '{request.url.path}' not allowed.")
        #     return JSONResponse(status_code=404, content={"detail": f"Route not found: {request.url.path}"})

        # 다음 미들웨어로 이동
        response = await call_next(request)
        return response