import jwt
import datetime
import secrets
import base64
from fastapi import APIRouter

router = APIRouter()

@router.get("/generate_secret_key")
def generate_secret_key():
    length = 32
    key = secrets.token_bytes(length)
    encoded_key = base64.urlsafe_b64encode(key).decode('utf-8')
    return encoded_key

secret_key = "gTA8B7V5W24-7jcn1IFoY0FHsBqgQ_Z6TWYD-J4Cyb4="

payload = {
    "user_id": "test@example.com",
    "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
}

def generate_jwt_token():
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("Generated Token:", token)

