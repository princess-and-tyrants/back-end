from fastapi import Request, APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.schemas.vote import Vote
from database_connect import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vote_dto import VoteReq
from sqlalchemy.future import select
from fastapi.security import APIKeyHeader
from app.services.vote_service import voteService

def verify_header(access_token=Security(APIKeyHeader(name='Authorization'))):
    return access_token

router = APIRouter()

@router.post("/vote", dependencies=[verify_header()], summary="투표 생성 api", description="", tags=["vote(투표)"])
async def create_vote(vote_req: VoteReq, request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)

    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await vote_service.create_vote(user.get("user_id"), vote_req.target_user_id, vote_req)
    return result

@router.get("/vote/result/my", dependencies=[verify_header()], summary="친구들이 생각하는 나의 mbti 결과 api", description="", tags=["vote(투표)"])
async def get_vote_my_result(request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)

    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await vote_service.get_vote_result(user.get("user_id"))
    return result

@router.get("/vote/list/my", dependencies=[verify_header()], summary="친구들이 생각하는 나의 mbti 방명록 api", description="", tags=["vote(투표)"])
async def get_vote_my_list(request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)

    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await vote_service.get_vote_list(user.get("user_id"))
    return result

@router.get("/home/vote/result/{user_id}", dependencies=[verify_header()], summary="친구들이 생각하는 나의 mbti 결과 api", description="", tags=["vote(투표)"])
async def get_vote_result(user_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)
    
    result = await vote_service.get_vote_result(user_id)
    return result

@router.get("/home/vote/list/{user_id}", dependencies=[verify_header()], summary="친구들이 생각하는 나의 mbti 방명록 api", description="", tags=["vote(투표)"])
async def get_vote_list(user_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    vote_service = voteService(db)
    
    result = await vote_service.get_vote_list(user_id)
    return result


# @router.post("/vote/{user_id}/new")
# async def create_vote_route(user_id: str, vote_req: VoteReq, db: Session = Depends(get_db)):
#     query = select(User).where(User.id == user_id, User.is_deleted == "N")
#     result = await db.execute(query)
#     user_exists = result.scalars().first()

#     # 유저가 존재하지 않으면 예외 처리
#     if not user_exists:
#         raise HTTPException(status_code=450, detail="User not found")

#     # create_vote 호출
#     result = await create_vote(db=db, vote_req=vote_req,user_id=user_id)
#     return result

# @router.get("/vote/{vote_id}")
# async def get_vote(vote_id: str, db: AsyncSession = Depends(get_db)):
#     result = await get_vote_by_id(db=db, vote_id=vote_id)
#     if not result:
#         raise HTTPException(status_code=450, detail="Vote not found")
#     return result

# @router.get("/votes/statistics/{user_id}")
# async def vote_statistics(user_id: str, db: AsyncSession = Depends(get_db)):
#     stats = await get_detailed_vote_statistics(db, user_id)
#     if stats["total_votes"] == 0:
#         raise HTTPException(status_code=404, detail="No votes found for the given user")
#     return stats