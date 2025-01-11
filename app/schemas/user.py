from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, index=True, comment="UUID")
    id = Column(String, unique=True, nullable=False, comment="사용자 ID, 고유 값")
    mbti_ei_score = Column(Integer, nullable=False, comment="MBTI 첫 번째 요소 (E,I) 점수")
    mbti2_sn_score = Column(Integer, nullable=False, comment="MBTI 두 번째 요소 (S,N) 점수")
    mbti3_tf_score = Column(Integer, nullable=False, comment="MBTI 세 번째 요소 (T,F) 점수")
    mbti4_pj_score = Column(Integer, nullable=False, comment="MBTI 네 번째 요소 (P,J) 점수")
    nickname = Column(String, nullable=False, comment="닉네임")
    password = Column(String, nullable=False, comment="비밀번호 (암호화된 해시 사용)")
    created_date = Column(DateTime, nullable=False, comment="생성일")
    modified_date = Column(DateTime, nullable=True, comment="수정일")
    is_deleted = Column(String, nullable=False, default="N", comment="삭제 여부 ('N': 활성, 'Y': 삭제됨)")
