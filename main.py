from fastapi import Depends, FastAPI, Request
from datetime import datetime
from sqlalchemy import text
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from app.schemas.vote import Vote
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# 모듈 추가
from database_connect import get_db
from app.routers.test_router import router as test_router
from app.routers.vote_router import router as vote_router
from app.utils.jwt_token_generator import router as jwt_token_generator
from jwt_middleware import JWTMiddleware, BlockUndefinedRoutesMiddleware
from app.utils.aes_logic import router as aes_logic
from app.routers.auth_router import router as auth_router
from app.routers.home_router import router as home_router
from app.routers.update_router import router as update_router
from app.routers.cardcase_router import router as cardcase_router


app = FastAPI(title="Hackathon Project", version="1.0")

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# 라우터 추가
app.include_router(test_router)
app.include_router(vote_router)
app.include_router(jwt_token_generator)
app.include_router(aes_logic)
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(update_router)
app.include_router(cardcase_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mbtid.winterholic.net", "http://localhost:5173"],  # 프론트 origin 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


# 허용된 경로 및 접두사 설정
allowed_routes = ["/user", "/cardcase", "/vote", "/my", "/home"]
excluded_prefixes = ["/signup", "/signin", "/check/id", "/home",
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
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)


# pip install -r requirements.txt

# uvicorn main:app --reload
# uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile=key.pem --ssl-certfile=cert.pem

#pip install --upgrade fastapi
#uvicorn main:app --host 0.0.0.0 --port 8000 --reload
#uvicorn main:app --host 0.0.0.0 --port 80 --reload

# ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '0000';