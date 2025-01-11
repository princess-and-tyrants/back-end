from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import mapped_column, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    posts = relationship("Post",back_populates="owner", cascade='delete')
    is_active = mapped_column(Boolean,default=False)

class Post(Base):
    __tablename__ = "posts"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255))
    owner_id = mapped_column(Integer, ForeignKey("users.id"))
    owner = relationship("User",back_populates="posts")