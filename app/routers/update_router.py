from app.models.auth_dto import SignupReq, SigninReq
from sqlalchemy.ext.asyncio import AsyncSession
from database_connect import get_db
from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException, Security
from app.services.user_sevice import UserService
from fastapi.security import APIKeyHeader
from app.models.user_dto import UpdateUserReq

router = APIRouter()

@router.get("/profile/update_nickname", summary="유저 정보 업데이트", description="", tags=["Update"])
async def get_home_profile(request: Request, update_user_req: UpdateUserReq, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await user_service.update_user_profile(user.get("user_id"), update_user_req)
    return result