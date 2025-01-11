import jwt
import datetime
import secrets
import base64
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/generate_secret_key")
def generate_secret_key():
    length = 32
    key = secrets.token_bytes(length)
    encoded_key = base64.urlsafe_b64encode(key).decode('utf-8')
    return encoded_key

secret_key = "gTA8B7V5W24-7jcn1IFoY0FHsBqgQ_Z6TWYD-J4Cyb4="

@router.get("/generate_jwt_token")
def generate_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("Generated Token:", token)