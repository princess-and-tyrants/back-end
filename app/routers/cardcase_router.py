from app.models.auth_dto import SignupReq, SigninReq
from sqlalchemy.ext.asyncio import AsyncSession
from database_connect import get_db
from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException, Security
from app.services.user_sevice import UserService
from app.services.cardcase_service import CardcaseService
from fastapi.security import APIKeyHeader

router = APIRouter()

@router.get("/cardcase", summary="보관함 조회 api", description="", tags=["Cardcase"])
async def get_cardcase_list(request: Request, db: AsyncSession = Depends(get_db)):
    cardcase_service = CardcaseService(db)
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await cardcase_service.get_cardcase_list(user.get("user_id"))
    return result

@router.post("/cardcase", summary="보관함 추가 api", description="", tags=["Cardcase"])
async def create_cardcase(request: Request, target_user_id: str, db: AsyncSession = Depends(get_db)):
    print(target_user_id)
    cardcase_service = CardcaseService(db)

    # 사용자 정보 확인
    user = getattr(request.state, "user", None)
    if not user or not user.get("user_id"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # 카드케이스 생성
    result = await cardcase_service.create_cardcase(user.get("user_id"), target_user_id)
    return result

@router.delete("/cardcase/{cardcase_id}", summary="보관함 삭제 API", description="물리적으로 카드케이스 데이터를 삭제", tags=["Cardcase"])
async def delete_cardcase(cardcase_id: str, db: AsyncSession = Depends(get_db)):
    cardcase_service = CardcaseService(db)
    result = await cardcase_service.delete_cardcase(cardcase_id)
    return result