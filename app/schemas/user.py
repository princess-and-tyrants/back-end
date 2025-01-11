from sqlalchemy import Column, Integer, String
from database_connect import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "user"

    # Columns
    user_id = Column(String(50), primary_key=True, index=True, comment="UUID")
    id = Column(String(50), unique=True, nullable=False, comment="사용자 ID, 고유 값")
    mbti_ei_score = Column(Integer, nullable=False, comment="MBTI 1번째 (E,I) [0(100)~100(0)]")
    mbti2_sn_score = Column(Integer, nullable=False, comment="MBTI 2번째 (S,N) [0(100)~100(0)]")
    mbti3_tf_score = Column(Integer, nullable=False, comment="MBTI 3번째 (F,T) [0(100)~100(0)]")
    mbti4_pj_score = Column(Integer, nullable=False, comment="MBTI 4번째 (P,J) [0(100)~100(0)]")
    nickname = Column(String(50), nullable=False, comment="닉네임")
    password = Column(String(255), nullable=False, comment="비밀번호 (암호화된 해시 사용)")
    created_date = Column(DateTime, nullable=False, server_default=func.now(), comment="생성일")
    modified_date = Column(DateTime, nullable=True, onupdate=func.now(), comment="수정일")
    is_deleted = Column(String(1), nullable=False, default="N", comment="삭제 여부 ('N': 활성, 'Y': 삭제됨)")

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', id='{self.id}', nickname='{self.nickname}')>"