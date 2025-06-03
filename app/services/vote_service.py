import uuid
import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.vote_dto import VoteReq
from app.schemas.user import User
from app.schemas.vote import Vote
from app.schemas.vote_link import VoteLink
from sqlalchemy import func

class voteService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_vote(self, voting_user_id: str, voted_user_id: str, VoteReq: VoteReq):
        try:
            # VoteLink 객체 조회 또는 생성
            query = select(VoteLink).where(VoteLink.target_user_id == voted_user_id)
            result = await self.db.execute(query)
            new_vote_link = result.scalars().first()

            if new_vote_link is None:
                new_vote_link = VoteLink(
                    link_id=str(uuid.uuid4()),
                    target_user_id=voted_user_id
                )
                self.db.add(new_vote_link)
                await self.db.commit()
                await self.db.refresh(new_vote_link)

            new_vote = Vote(
                vote_id=str(uuid.uuid4()),  # UUID 생성
                voting_user_id=voting_user_id,
                link_id=new_vote_link.link_id,
                first_mbti_element=VoteReq.first_mbti_element,
                second_mbti_element=VoteReq.second_mbti_element,
                third_mbti_element=VoteReq.third_mbti_element,
                forth_mbti_element=VoteReq.forth_mbti_element,
                comment=VoteReq.comment,
                incognito=VoteReq.incognito
            )
            self.db.add(new_vote)  # 세션에 추가
            await self.db.commit()  # 트랜잭션 커밋
            await self.db.refresh(new_vote)  # 새로 생성된 Vote 객체를 갱신
            # 성공적인 삽입 후 반환 데이터 구성
            
            # 성공적인 삽입 후 반환 데이터 구성
            return {
                "message": "cardcase created successfully",
                "data": {
                    "vote_id": new_vote.vote_id
                }
            }
        
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="투표 결과 데이터 생성중에 오류가 발생했습니다. 다시 시도해주세요.")
    
    async def get_vote_result(self, user_id : str):
        # VoteLink 객체 조회
        query = select(VoteLink).where(VoteLink.target_user_id == user_id)
        result = await self.db.execute(query)
        user_vote_link = result.scalars().first()

        if user_vote_link is None:
            user_vote_link = VoteLink(
                link_id=str(uuid.uuid4()),
                target_user_id=user_id,
                is_deleted="N"
            )
            self.db.add(user_vote_link)
            await self.db.commit()
            await self.db.refresh(user_vote_link)

        query = select(Vote).where(Vote.link_id == user_vote_link.link_id, Vote.is_deleted == "N")
        result = await self.db.execute(query)
        user_vote = result.scalars().all()

        mbti_ei_score = 0
        mbti_sn_score = 0
        mbti_tf_score = 0
        mbti_jp_score = 0
        mbti_result = None

        mbti_i_count = 0
        mbti_n_count = 0
        mbti_f_count = 0
        mbti_p_count = 0

        total_count = 0

        for vote in user_vote:
            total_count += 1

            if vote.first_mbti_element == "I":
                mbti_i_count += 1
            if vote.second_mbti_element == "N":
                mbti_n_count += 1
            if vote.third_mbti_element == "F":
                mbti_f_count += 1
            if vote.forth_mbti_element == "P":
                mbti_p_count += 1
            
        # MBTI 점수 계산
        if total_count > 0:
            mbti_ei_score = (mbti_i_count / total_count) * 100
            mbti_sn_score = (mbti_n_count / total_count) * 100
            mbti_tf_score = (mbti_f_count / total_count) * 100
            mbti_jp_score = (mbti_p_count / total_count) * 100

            mbti_result = ""
            mbti_result += "E" if mbti_ei_score < 50 else "I"
            mbti_result += "S" if mbti_sn_score < 50 else "N"
            mbti_result += "T" if mbti_tf_score < 50 else "F"
            mbti_result += "J" if mbti_jp_score < 50 else "P"
        else:
            mbti_result = None
        

        # 성공적인 삽입 후 반환 데이터 구성
        return {
            "message": "cardcase created successfully",
            "data": {
                "total_count": total_count,
                "mbti_ei_score": mbti_ei_score,
                "mbti_sn_score": mbti_sn_score,
                "mbti_tf_score": mbti_tf_score,
                "mbti_jp_score": mbti_jp_score,
                "mbti_result": mbti_result
            }
        }
    
    async def get_vote_list(self, user_id : str):
        # VoteLink 객체 조회
        query = select(VoteLink).where(VoteLink.target_user_id == user_id)
        result = await self.db.execute(query)
        user_vote_link = result.scalars().first()

        if user_vote_link is None:
            user_vote_link = VoteLink(
                link_id=str(uuid.uuid4()),
                target_user_id=user_id,
                is_deleted="N"
            )
            self.db.add(user_vote_link)
            await self.db.commit()
            await self.db.refresh(user_vote_link)

        query = select(Vote).where(Vote.link_id == user_vote_link.link_id, Vote.is_deleted == "N")
        result = await self.db.execute(query)
        user_vote = result.scalars().all()

        # voting_user_id를 기준으로 유저 정보 조회 및 딕셔너리 생성
        voting_user_ids = list(set([vote.voting_user_id for vote in user_vote]))

        query = select(User).where(User.user_id.in_(voting_user_ids), User.is_deleted == "N")
        result = await self.db.execute(query)
        users = result.scalars().all()
        user_dict = {user.user_id: user.nickname for user in users}

        result_list = []
        
        for vote in user_vote:
            mbti_result = ""
            mbti_result += vote.first_mbti_element
            mbti_result += vote.second_mbti_element
            mbti_result += vote.third_mbti_element
            mbti_result += vote.forth_mbti_element

            user_vote_dict = {
                "vote_id": vote.vote_id,
                "voting_user_id": vote.voting_user_id,
                "voting_user_nickname": user_dict.get(vote.voting_user_id, "Unknown"),
                "mbti_result": mbti_result,
                "comment": vote.comment,
                "incognito": vote.incognito
            }
            result_list.append(user_vote_dict)

        # 성공적인 삽입 후 반환 데이터 구성
        return {
            "message": "cardcase created successfully",
            "data": result_list
        }





























# # 로깅 설정
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# async def find_user_id(db: AsyncSession, id: str):
#     logger.info(f"find_user_id() 호출 - 입력 ID: {id}")
    
#     query = select(User).where(User.id == id, User.is_deleted == "N")
#     result = await db.execute(query)
#     user = result.scalars().first()
    
#     if not user:
#         logger.error(f"User not found with ID: {id}")
#         raise HTTPException(status_code=450, detail="User not found")

#     logger.info(f"User found: {user}")
#     return user.user_id

# async def find_link(db: AsyncSession, id: str):
#     logger.info(f"find_link() 호출 - 입력 ID: {id}")
    
#     user_id = await find_user_id(db, id)
#     logger.info(f"find_user_id() 결과 - User ID: {user_id}")
    
#     query = select(VoteLink).where(VoteLink.target_user_id == user_id, VoteLink.is_deleted == "N")
#     result = await db.execute(query)
#     link = result.scalars().first()
    
#     if not link:
#         logger.error(f"Vote link not found for User ID: {user_id}")
#         raise HTTPException(status_code=451, detail="Vote link not found")

#     logger.info(f"Vote link found: {link}")
#     return link.link_id

# async def create_vote(db: AsyncSession, vote_req: VoteReq, user_id: str):
#     logger.info(f"create_vote() 호출 - User ID: {user_id}, Vote Request: {vote_req}")
    
#     try:
#         voting_user_id = await find_user_id(db, user_id)
#         logger.info(f"find_user_id() 결과 - Voting User ID: {voting_user_id}")
        
#         link_id = await find_link(db, user_id)
#         logger.info(f"find_link() 결과 - Link ID: {link_id}")
#     except HTTPException as e:
#         logger.error(f"Error in creating vote: {e.detail}")
#         raise

#     new_vote = Vote(
#         vote_id=str(uuid.uuid4()),
#         voting_user_id=voting_user_id,
#         link_id=link_id,
#         first_mbti_element=vote_req.first_mbti_element,
#         second_mbti_element=vote_req.second_mbti_element,
#         third_mbti_element=vote_req.third_mbti_element,
#         forth_mbti_element=vote_req.forth_mbti_element,
#         comment=vote_req.comment,
#         incognito=vote_req.incognito
#     )
    
#     logger.info(f"New vote object created: {new_vote}")
    
#     db.add(new_vote)
#     await db.commit()
#     await db.refresh(new_vote)
    
#     logger.info(f"Vote successfully created: {new_vote}")
#     return {"message": "Vote created successfully"}

# async def get_vote_by_id(db: AsyncSession, vote_id: str):
#     logger.info(f"get_vote_by_id() 호출 - Vote ID: {vote_id}")
    
#     query = select(Vote).where(
#         Vote.vote_id == vote_id,
#         Vote.is_deleted == "N"
#     )
#     result = await db.execute(query)
#     vote = result.scalars().first()
    
#     if not vote:
#         logger.error(f"Vote not found with ID: {vote_id}")
#         raise HTTPException(status_code=450, detail="Vote not found")

#     logger.info(f"Vote found: {vote}")
#     return vote

# async def get_detailed_vote_statistics(db: AsyncSession, user_id: str):
#     voting_user_id = await find_user_id(db,user_id)
#     if not voting_user_id :
#         raise HTTPException(status_code=450, detail="User not found")
#     # 총 투표 개수 구하기
#     total_votes_query = select(func.count()).where(
#         Vote.voting_user_id == voting_user_id,
#         Vote.is_deleted == "N"
#     )
#     total_votes_result = await db.execute(total_votes_query)
#     total_votes = total_votes_result.scalar()

#     if total_votes == 0:
#         return {
#             "total_votes": 0,
#             "mbti_statistics": {
#                 "first_mbti_element": {},
#                 "second_mbti_element": {},
#                 "third_mbti_element": {},
#                 "forth_mbti_element": {}
#             }
#         }

#     # MBTI 통계 구하는 공통 함수
#     async def get_mbti_element_stats(element_column):
#         query = select(
#             element_column,
#             func.count().label("count")
#         ).where(
#             Vote.voting_user_id == voting_user_id,
#             Vote.is_deleted == "N"
#         ).group_by(element_column)

#         result = await db.execute(query)
#         return {row[0]: (row[1] / total_votes) * 100 for row in result}

#     # 각 MBTI 요소별 통계 구하기
#     first_stats = await get_mbti_element_stats(Vote.first_mbti_element)
#     second_stats = await get_mbti_element_stats(Vote.second_mbti_element)
#     third_stats = await get_mbti_element_stats(Vote.third_mbti_element)
#     forth_stats = await get_mbti_element_stats(Vote.forth_mbti_element)

#     return {
#         "total_votes": total_votes,
#         "mbti_statistics": {
#             "first_mbti_element": first_stats,
#             "second_mbti_element": second_stats,
#             "third_mbti_element": third_stats,
#             "forth_mbti_element": forth_stats
#         }
#     }