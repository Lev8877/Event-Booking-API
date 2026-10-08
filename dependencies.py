import os 
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from models.users import User 

from jwt.exceptions import InvalidTokenError
import jwt



load_dotenv() 

database_url = os.getenv("DATABASE_URL")

engine = create_async_engine(database_url)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

async def get_session():
    async with SessionLocal() as session:
        yield session

async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        token_type = payload.get('type')
        sub = payload.get('sub')

        if not token_type:
            raise HTTPException(status_code=401, detail='Invalid Credentials')

        if token_type != 'access':
            raise HTTPException(status_code=401, detail='Invalid Credentials')
        
        if sub is None:
            raise HTTPException(status_code=401, detail='Invalid Credentials')

        user_id = int(sub)

        statement = await session.execute(select(User).where(User.id == user_id))
        user = statement.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=401, detail='Invalid Credentials') 

        return user 

    except (InvalidTokenError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail='Invalid Credentials') 

        