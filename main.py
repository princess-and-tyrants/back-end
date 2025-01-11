from fastapi import FastAPI
from datetime import datetime


# 모듈 추가
from app.routers.test_router import router as test_router
from app.utils.jwt_token_generator import router as jwt_token_generator
from jwt_middleware import JWTMiddleware, BlockUndefinedRoutesMiddleware

app = FastAPI(title="Hackathon Project", version="1.0")

# 라우터 추가
app.include_router(test_router)
app.include_router(jwt_token_generator)

# 허용된 경로 및 접두사 설정
allowed_routes = ["/", "/docs", "/redoc", "/openapi.json"]
excluded_prefixes = ["/public", "/static"]

# 미들웨어 추가
app.add_middleware(JWTMiddleware, excluded_prefixes=excluded_prefixes)
app.add_middleware(BlockUndefinedRoutesMiddleware, allowed_routes=allowed_routes, excluded_prefixes=excluded_prefixes)

@app.get("/")
def read_root():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": current_time}




#pip install fastapi uvicorn aioredis pymysql sqlalchemy databases PYJWT python-dotenv pydantic-settings starlette
#uvicorn main:app --reload
#pip install --upgrade fastapi