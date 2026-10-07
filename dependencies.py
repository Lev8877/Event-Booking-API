import os 
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv() 

database_url = os.getenv("DATABASE_URL")

engine = create_async_engine(database_url)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session():
    async with SessionLocal() as session:
        yield session