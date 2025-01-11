import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.vote import VoteReq
from app.schemas import user
from app.schemas.vote import Vote
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import User
from app.schemas.vote_link import VoteLink

async def find_user_id(db: AsyncSession, id: str):
    # User 테이블에서 id로 사용자 검색
    query = select(User).where(User.id == id, User.is_deleted == "N")
    result = await db.execute(query)  # 비동기 실행
    user = result.scalars().first()

    # 사용자 존재하지 않으면 예외 처리
    if not user:
        raise HTTPException(status_code=450, detail="User not found")

    return user.user_id

async def find_link(db: AsyncSession, id: str) :
    # 먼저 user_id를 찾아야 하므로 find_user_id 호출
    user_id = await find_user_id(db, id)
    
    # user_id로 link를 찾는 쿼리 작성
    link_query = select(Vote).where(Vote.voting_user_id == user_id)
    result = await db.execute(link_query)  # 비동기 실행
    link_db = result.scalars().first()  # 첫 번째 결과 추출

    # link가 없다면 예외 처리
    if not link_db:
        raise HTTPException(status_code=451, detail="Vote link not found")

    return link_db.link_id

async def create_vote(db: AsyncSession,vote_req: VoteReq,user_id:str):
    new_vote = Vote(
        vote_id=str(uuid.uuid4()),  # 실제 투표 ID 생성 방법을 구현
        voting_user_id=find_user_id(db,user_id),
        link_id=find_link(db,user_id),
        first_mbti_element=vote_req.first_mbti_element,
        second_mbti_element=vote_req.second_mbti_element,
        third_mbti_element=vote_req.third_mbti_element,
        forth_mbti_element=vote_req.forth_mbti_element,
        comment=vote_req.comment,
        incognito=vote_req.incognito,
        is_deleted="N",  # 기본값 설정 (삭제되지 않음)
    )
    db.add(new_vote)
    await db.commit()  # 비동기 커밋
    await db.refresh(new_vote)
    return new_vote

async def get_vote_by_id(db: AsyncSession, vote_id: str):
    query = select(Vote).where(
        Vote.vote_id == vote_id, 
        Vote.is_deleted == "N"
    )
    result = await db.execute(query)  # 비동기 실행
    return result.scalars().first()  # 결과를 추출