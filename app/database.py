from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("DB_USER")     # "root"
passwd = os.getenv("DB_PASSWD") # "0000"
host = os.getenv("DB_HOST")     # "127.0.0.1"
port = os.getenv("DB_PORT")     # "3306"
db = os.getenv("DB_NAME")       # "mydb"

DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'

engine = create_engine(DB_URL, echo=True) #echo로 쿼리 확인 가능
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
Base = declarative_base()