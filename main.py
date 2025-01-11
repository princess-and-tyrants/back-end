from fastapi import FastAPI, Request
from datetime import datetime
import logging


# 모듈 추가
from app.routers.test_router import router as test_router
from app.utils.jwt_token_generator import router as jwt_token_generator
from jwt_middleware import JWTMiddleware, BlockUndefinedRoutesMiddleware

app = FastAPI(title="Hackathon Project", version="1.0")

logging.basicConfig(level=logging.DEBUG)

# 라우터 추가
app.include_router(test_router)
app.include_router(jwt_token_generator)

# 허용된 경로 및 접두사 설정
allowed_routes = []
excluded_prefixes = ["/public", "/static", "/docs", "/redoc", "/openapi.json"]

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



#pip install fastapi uvicorn aioredis pymysql sqlalchemy databases PYJWT python-dotenv pydantic-settings starlette
#uvicorn main:app --reload
#pip install --upgrade fastapi