from fastapi import FastAPI
from routers import test_router

app = FastAPI(title="Hackathon Project", version="1.0")

# 라우터 추가
app.include_router(test_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon Project!"}