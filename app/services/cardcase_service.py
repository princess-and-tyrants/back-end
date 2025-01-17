import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.user import User
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from sqlalchemy import and_, update
from sqlalchemy.exc import SQLAlchemyError
from app.models.auth_dto import SignupReq, SigninReq
from app.utils.aes_logic import key, iv, aes_decrypt
import bcrypt
from app.utils.jwt_token_generator import generate_jwt_token
from app.models.user_dto import UpdateUserNicknameReq, UpdateUserMbtiReq
from datetime import datetime
from app.schemas.cardcase import CardCase

class CardcaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def delete_cardcase(self, cardcase_id: str):
        try:
            # 삭제할 CardCase 레코드 조회
            result = await self.db.execute(select(CardCase).where(CardCase.cardcase_id == cardcase_id))
            cardcase = result.scalar_one_or_none()

            # 존재하지 않는 경우
            if not cardcase:
                raise HTTPException(status_code=404, detail="CardCase not found")

            # 레코드 삭제
            await self.db.delete(cardcase)
            await self.db.commit()

            return {"message": "cardcase deleted successfully"}

        except Exception as e:
            # 예외 발생 시 롤백
            await self.db.rollback()
            print(f"Error occurred during deletion: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete cardcase due to a server error.")

    async def create_cardcase(self, this_owner_user_id: str, this_collected_user_id: str):
        try:
            # 새 CardCase 객체 생성
            new_cardcase = CardCase(
                cardcase_id=str(uuid.uuid4()),  # UUID 생성
                owner_user_id=this_owner_user_id,
                collected_user_id=this_collected_user_id
            )
            self.db.add(new_cardcase)  # 세션에 추가
            await self.db.commit()  # 트랜잭션 커밋
            
            # DB 커밋 후, 생성된 날짜를 다시 읽음
            await self.db.refresh(new_cardcase)
            
            # 성공적인 삽입 후 반환 데이터 구성
            return {
                "message": "cardcase created successfully",
                "data": {
                    "cardcase_id": new_cardcase.cardcase_id,
                    "owner_user_id": new_cardcase.owner_user_id,
                    "collected_user_id": new_cardcase.collected_user_id,
                    "created_date": new_cardcase.created_date.isoformat(),
                }
            }
        
        except Exception as e:
            # 예외 발생 시 롤백 및 디버깅 로그 출력
            await self.db.rollback()
            print(f"Error occurred during transaction: {e}")
            raise HTTPException(status_code=500, detail="Failed to create cardcase due to a server error.")
            
    
    async def get_cardcase_list(self, user_id : str):
        query = select(User).where(and_(User.user_id == user_id, User.is_deleted == "N"))
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=450, detail="Resource not found") # 450 : 해당 데이터
        
        new_query1 = select(CardCase).where(and_(CardCase.owner_user_id == user_id, CardCase.is_deleted == "N"))
        result = await self.db.execute(new_query1)
        cardcase_records = result.scalars().all()

        collected_user_ids = [record.collected_user_id for record in cardcase_records]
        print(collected_user_ids)
        if collected_user_ids:
            new_query2 = select(User).where(User.user_id.in_(collected_user_ids))
            result = await self.db.execute(new_query2)
            user_records = result.scalars().all()

            cardcase_data = []
            print(user_records)
            for ur in user_records :
                mbti_first_element = 'I' if ur.mbti_ei_score > 50 else 'E'
                mbti_second_element = 'N' if ur.mbti_sn_score > 50 else 'S'
                mbti_third_element = 'F' if ur.mbti_tf_score > 50 else 'T'
                mbti_forth_element = 'J' if ur.mbti_pj_score > 50 else 'P'

                temp_dict = {}
                temp_dict["user_id"] = ur.user_id
                temp_dict["nickname"] = ur.nickname
                temp_dict["mbti"] = mbti_first_element + mbti_second_element + mbti_third_element + mbti_forth_element
                temp_dict["mbti_ei_score"] = ur.mbti_ei_score
                temp_dict["mbti_sn_score"] = ur.mbti_sn_score
                temp_dict["mbti_tf_score"] = ur.mbti_tf_score
                temp_dict["mbti_pj_score"] = ur.mbti_pj_score
                cardcase_data.append(temp_dict)

            return {"message" : "It is okay", "data" : cardcase_data}
        
        return {"message" : "no data in cardcase"}