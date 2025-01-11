from fastapi import Depends, FastAPI, Request
from datetime import datetime
from sqlalchemy import text
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


# 모듈 추가
from app.routers.test_router import router as test_router
from app.utils.jwt_token_generator import router as jwt_token_generator
from jwt_middleware import JWTMiddleware, BlockUndefinedRoutesMiddleware
from database_connect import get_db
from app.utils.aes_logic import router as aes_logic


app = FastAPI(title="Hackathon Project", version="1.0")


logging.basicConfig(level=logging.DEBUG)


# 라우터 추가
app.include_router(test_router)
app.include_router(jwt_token_generator)
app.include_router(aes_logic)


# 허용된 경로 및 접두사 설정
allowed_routes = []
excluded_prefixes = ["/", "/users" ,"/public", "/static", "/docs", "/redoc", "/openapi.json", "/generate_secret_key", "/generate_key", "/generate_key_base64"]


# 미들웨어 추가
app.add_middleware(JWTMiddleware,
    allowed_routes=allowed_routes,
    excluded_prefixes=excluded_prefixes,)
app.add_middleware(
    BlockUndefinedRoutesMiddleware,
    allowed_routes=allowed_routes,
    excluded_prefixes=excluded_prefixes,
)


@app.get("/")
def read_root():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": current_time}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.debug(f"Request URL: {request.url.path}")
    response = await call_next(request)
    logging.debug(f"Response Status: {response.status_code}")
    return response


@app.get("/users/") #테스트용 모든 users데이터 전부 조회
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM user"))  # 모든 데이터를 조회
    users = [dict(row._mapping) for row in result.fetchall()]  # 딕셔너리로 변환
    return users


#pip install fastapi uvicorn aioredis pymysql sqlalchemy databases PYJWT python-dotenv pydantic-settings starlette aiomysql
#uvicorn main:app --reload
#pip install --upgrade fastapi