from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+aiomysql://root:0000@db:3306/mbtid"
# DATABASE_URL = "mysql+aiomysql://root:0000@127.0.0.1:3306/mbtid"
# DATABASE_URL = "mysql+aiomysql://root:0000@:3306/mbtid"

Base = declarative_base()

# SQLAlchemy 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 종속성 함수
async def get_db():
    async with SessionLocal() as session:
        yield session