import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.user import User
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from sqlalchemy import and_
from app.models.auth_dto import SignupReq, SigninReq
from app.utils.aes_logic import key, iv, aes_decrypt
import bcrypt
from app.utils.jwt_token_generator import generate_jwt_token



class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

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