from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.schemas.vote import Vote
from app.services.vote_service import get_vote_by_id,create_vote
from database_connect import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vote import VoteReq
from sqlalchemy.future import select

router = APIRouter()

@router.post("/{user_id}/vote/new")
async def create_vote_route(user_id: str, vote_req: VoteReq, db: Session = Depends(get_db)):
    query = select(User).where(User.id == user_id, User.is_deleted == "N")
    result = await db.execute(query)
    user_exists = result.scalars().first()

    # 유저가 존재하지 않으면 예외 처리
    if not user_exists:
        raise HTTPException(status_code=450, detail="User not found")

    # create_vote 호출
    result = await create_vote(db=db, vote_req=vote_req,user_id=user_id)
    return result

@router.get("/{vote_id}")
async def get_vote(vote_id: str, db: AsyncSession = Depends(get_db)):
    result = await get_vote_by_id(db=db, vote_id=vote_id)
    if not result:
        raise HTTPException(status_code=450, detail="Vote not found")
    return result