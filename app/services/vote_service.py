import uuid
import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.vote import VoteReq
from app.schemas.user import User
from app.schemas.vote import Vote
from app.schemas.vote_link import VoteLink
from sqlalchemy import func

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def find_user_id(db: AsyncSession, id: str):
    logger.info(f"find_user_id() 호출 - 입력 ID: {id}")
    
    query = select(User).where(User.id == id, User.is_deleted == "N")
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        logger.error(f"User not found with ID: {id}")
        raise HTTPException(status_code=450, detail="User not found")

    logger.info(f"User found: {user}")
    return user.user_id

async def find_link(db: AsyncSession, id: str):
    logger.info(f"find_link() 호출 - 입력 ID: {id}")
    
    user_id = await find_user_id(db, id)
    logger.info(f"find_user_id() 결과 - User ID: {user_id}")
    
    query = select(VoteLink).where(VoteLink.target_user_id == user_id, VoteLink.is_deleted == "N")
    result = await db.execute(query)
    link = result.scalars().first()
    
    if not link:
        logger.error(f"Vote link not found for User ID: {user_id}")
        raise HTTPException(status_code=451, detail="Vote link not found")

    logger.info(f"Vote link found: {link}")
    return link.link_id

async def create_vote(db: AsyncSession, vote_req: VoteReq, user_id: str):
    logger.info(f"create_vote() 호출 - User ID: {user_id}, Vote Request: {vote_req}")
    
    try:
        voting_user_id = await find_user_id(db, user_id)
        logger.info(f"find_user_id() 결과 - Voting User ID: {voting_user_id}")
        
        link_id = await find_link(db, user_id)
        logger.info(f"find_link() 결과 - Link ID: {link_id}")
    except HTTPException as e:
        logger.error(f"Error in creating vote: {e.detail}")
        raise

    new_vote = Vote(
        vote_id=str(uuid.uuid4()),
        voting_user_id=voting_user_id,
        link_id=link_id,
        first_mbti_element=vote_req.first_mbti_element,
        second_mbti_element=vote_req.second_mbti_element,
        third_mbti_element=vote_req.third_mbti_element,
        forth_mbti_element=vote_req.forth_mbti_element,
        comment=vote_req.comment,
        incognito=vote_req.incognito
    )
    
    logger.info(f"New vote object created: {new_vote}")
    
    db.add(new_vote)
    await db.commit()
    await db.refresh(new_vote)
    
    logger.info(f"Vote successfully created: {new_vote}")
    return {"message": "Vote created successfully"}

async def get_vote_by_id(db: AsyncSession, vote_id: str):
    logger.info(f"get_vote_by_id() 호출 - Vote ID: {vote_id}")
    
    query = select(Vote).where(
        Vote.vote_id == vote_id,
        Vote.is_deleted == "N"
    )
    result = await db.execute(query)
    vote = result.scalars().first()
    
    if not vote:
        logger.error(f"Vote not found with ID: {vote_id}")
        raise HTTPException(status_code=450, detail="Vote not found")

    logger.info(f"Vote found: {vote}")
    return vote

async def get_detailed_vote_statistics(db: AsyncSession, user_id: str):
    voting_user_id = await find_user_id(db,user_id)
    if not voting_user_id :
        raise HTTPException(status_code=450, detail="User not found")
    # 총 투표 개수 구하기
    total_votes_query = select(func.count()).where(
        Vote.voting_user_id == voting_user_id,
        Vote.is_deleted == "N"
    )
    total_votes_result = await db.execute(total_votes_query)
    total_votes = total_votes_result.scalar()

    if total_votes == 0:
        return {
            "total_votes": 0,
            "mbti_statistics": {
                "first_mbti_element": {},
                "second_mbti_element": {},
                "third_mbti_element": {},
                "forth_mbti_element": {}
            }
        }

    # MBTI 통계 구하는 공통 함수
    async def get_mbti_element_stats(element_column):
        query = select(
            element_column,
            func.count().label("count")
        ).where(
            Vote.voting_user_id == voting_user_id,
            Vote.is_deleted == "N"
        ).group_by(element_column)

        result = await db.execute(query)
        return {row[0]: (row[1] / total_votes) * 100 for row in result}

    # 각 MBTI 요소별 통계 구하기
    first_stats = await get_mbti_element_stats(Vote.first_mbti_element)
    second_stats = await get_mbti_element_stats(Vote.second_mbti_element)
    third_stats = await get_mbti_element_stats(Vote.third_mbti_element)
    forth_stats = await get_mbti_element_stats(Vote.forth_mbti_element)

    return {
        "total_votes": total_votes,
        "mbti_statistics": {
            "first_mbti_element": first_stats,
            "second_mbti_element": second_stats,
            "third_mbti_element": third_stats,
            "forth_mbti_element": forth_stats
        }
    }