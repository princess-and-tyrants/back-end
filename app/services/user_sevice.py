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
from app.models.user_dto import UpdateUserReq
import datetime


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_user_profile(self, user_id : str, update_user_req: UpdateUserReq) :
        async with self.db.begin() as transaction:  # 트랜잭션 시작
            try:
                # 기존 사용자 검색
                query = select(User).where(and_(User.user_id == user_id, User.is_deleted == "N"))
                result = await self.db.execute(query)
                user = result.scalar_one_or_none()

                if not user:
                    raise HTTPException(status_code=450, detail="Resource not found")  # 450 : 해당 데이터 없음

                # 업데이트 쿼리 작성
                update_query = (
                    update(User)
                    .where(User.user_id == user_id)
                    .values(
                        mbti_ei_score=update_user_req.mbti_ei_score,
                        mbti_sn_score=update_user_req.mbti_sn_score,
                        mbti_tf_score=update_user_req.mbti_tf_score,
                        mbti_pj_score=update_user_req.mbti_pj_score,
                        nickname=update_user_req.nickname,
                        modified_date=datetime.utcnow()  # 수정 날짜 갱신
                    )
                )

                # 업데이트 실행
                await self.db.execute(update_query)

            except HTTPException:
                # 특정 예외는 바로 전달
                raise
            except SQLAlchemyError as e:
                # SQLAlchemy 관련 에러 발생 시 롤백
                await transaction.rollback()
                raise HTTPException(status_code=404, detail="Database error occurred") from e


    async def get_home_profile(self, user_id : str):
        query = select(User).where(and_(User.user_id == user_id, User.is_deleted == "N"))
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=450, detail="Resource not found") # 450 : 해당 데이터 
        
        mbti_first_element = 'I' if user.mbti_ei_score > 50 else 'E'
        mbti_second_element = 'N' if user.mbti_sn_score > 50 else 'S'
        mbti_third_element = 'F' if user.mbti_tf_score > 50 else 'T'
        mbti_forth_element = 'J' if user.mbti_pj_score > 50 else 'P'

        mbti = mbti_first_element + mbti_second_element + mbti_third_element + mbti_forth_element

        return {"userId" : user.user_id, "nickname" : user.nickname, "mbti" : mbti}


    async def check_duplicate_id(self, id : str):
        query = select(exists().where(and_(User.id == id, User.is_deleted == "N")))
        result = await self.db.execute(query)
        is_duplicate = result.scalar()

        if is_duplicate:
            raise HTTPException(status_code=404, detail="Id is duplicated")
        
        return {"message": "Id is valid"}
    

    async def signup(self, signup_req: SignupReq):
        try:
            print(signup_req)
            decrypted_password = aes_decrypt(signup_req.password, key, iv)
            password_bytes = decrypted_password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            print(hashed_password)
            # UUID 자동 생성
            new_user = User(
                user_id=str(uuid.uuid4()),  # UUID 생성
                id=signup_req.id,  # UserReq에서 값 가져오기
                nickname=signup_req.nickname,
                password=hashed_password,  # 비밀번호는 해시 처리 필요
                mbti_ei_score=signup_req.mbti_ei_score,
                mbti_sn_score=signup_req.mbti_sn_score,
                mbti_tf_score=signup_req.mbti_tf_score,
                mbti_pj_score=signup_req.mbti_pj_score
            )

            # DB에 새 사용자 추가
            self.db.add(new_user)
            await self.db.commit()  # 트랜잭션 커밋
            return {"message": "User created successfully"}

        except Exception as e:
            await self.db.rollback()  # 에러 발생 시 롤백
            raise HTTPException(status_code=404, detail="signup is failed")

        finally:
            await self.db.close()  # 세션 닫기


    async def signin(self, signin_req: SigninReq):
        decrypted_password = aes_decrypt(signin_req.password, key, iv)
        query = select(User).where(and_(User.id == signin_req.id, User.is_deleted == "N"))
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=451, detail="Id not found") # 451 : id가 유효하지 않은 경우
            
        # 비밀번호 검증
        if not bcrypt.checkpw(decrypted_password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=452, detail="Password is invalid") # 452 : pw가 유효하지 않은 경우

        await self.db.close()  # 세션 닫기
        return {"accessToken" : generate_jwt_token(user.user_id)}