from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class VoteLink(Base):
    __tablename__ = "vote_link"

    link_id = Column(String, primary_key=True, index=True, comment="UUID (PK)")
    target_user_id = Column(String, ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="투표 대상 유저 ID (user 테이블 참조)")
    created_date = Column(DateTime, nullable=False, comment="생성일")
    modified_date = Column(DateTime, nullable=True, comment="수정일")
    is_deleted = Column(String, nullable=False, default="N", comment="삭제 여부 ('N': 활성, 'Y': 삭제됨)")
