from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException
from app.services.user_sevice import UserService
from app.models.auth_dto import SignupReq, SigninReq
from sqlalchemy.ext.asyncio import AsyncSession
from database_connect import get_db

router = APIRouter()

@router.post("/signup", tags=["Auth"])
async def signup(signup_req: SignupReq, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    try:
        result = await user_service.signup(signup_req)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="fail")
    
@router.post("/check/nickname", tags=["Auth"])
async def check_duplicate_id(id : str, db: AsyncSession = Depends(get_db)) :
    user_service = UserService(db)
    try :
        result = await user_service.check_duplicate_id()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="fail")
    
@router.post("/signin", tags=["Auth"])
async def signin(signin_req: SigninReq, db: AsyncSession = Depends(get_db)) :
    user_service = UserService(db)
    try :
        result = await user_service.signin(signin_req)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="fail")