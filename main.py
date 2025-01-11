from fastapi import FastAPI, Request, Depends, HTTPException
from datetime import datetime
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


#pip install fastapi uvicorn aioredis pymysql sqlalchemy databases PYJWT python-dotenv


from app.routers.test_router import router as test_router
from app.utils.jwt_token_generator import router as jwt_token_generator
from app.database import Base, engine, SessionLocal

def init_db():
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Hackathon Project", version="1.0")
init_db()


# 라우터 추가
app.include_router(test_router)
app.include_router(jwt_token_generator)

@app.get("/")
def read_root():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": current_time}

@app.get("/home")
def home_test(name: str, db: Session = Depends(get_db)):
    return name


# @app.middleware("http")




#uvicorn main:app --reload