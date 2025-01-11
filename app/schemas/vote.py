from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vote(Base):
    __tablename__ = "vote"

    vote_id = Column(String, primary_key=True, index=True)
    link_id = Column(String(255))
    voting_user_id = Column(String(255))
    first_mbti_element = Column(String)
    second_mbti_element = Column(String)
    third_mbti_element = Column(String)
    forth_mbti_element = Column(String)
    comment = Column(String(255))
    incognito = Column(String)
    created_date = Column(DateTime)
    modified_date = Column(DateTime)
    is_deleted = Column(String)