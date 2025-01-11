from fastapi import Depends, FastAPI, Request
from datetime import datetime
from sqlalchemy import text
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 모듈 추가
from app.routers.test_router import router as test_router
from app.utils.jwt_token_generator import router as jwt_token_generator
from jwt_middleware import JWTMiddleware, BlockUndefinedRoutesMiddleware
from app.utils.aes_logic import router as aes_logic
from app.routers.auth_router import router as auth_router
from app.routers.home_router import router as home_router
from app.routers.update_router import router as update_router


app = FastAPI(title="Hackathon Project", version="1.0")

logging.basicConfig(level=logging.DEBUG)


# 라우터 추가
app.include_router(test_router)
app.include_router(jwt_token_generator)
app.include_router(aes_logic)
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(update_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 허용된 경로 및 접두사 설정
allowed_routes = ["/home/profile", "/user/update_nickname", "/user/update_mbti"]
excluded_prefixes = ["/signup", "/signin", "/check/nickname",
                     "/public", "/static", "/docs", "/redoc", "/openapi.json", "/make_test_password",
                      "/generate_secret_key", "/generate_key", "/generate_key_base64"]


# 미들웨어 추가
app.add_middleware(JWTMiddleware,
    allowed_routes=allowed_routes,
    excluded_prefixes=excluded_prefixes,)
app.add_middleware(
    BlockUndefinedRoutesMiddleware,
    allowed_routes=allowed_routes,
    excluded_prefixes=excluded_prefixes,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.debug(f"Request URL: {request.url.path}")
    response = await call_next(request)
    logging.debug(f"Response Status: {response.status_code}")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


#pip install fastapi uvicorn aioredis pymysql sqlalchemy databases PYJWT python-dotenv pydantic-settings starlette aiomysql
#uvicorn main:app --reload
#pip install --upgrade fastapi
#uvicorn main:app --host 0.0.0.0 --port 8000 --reload
