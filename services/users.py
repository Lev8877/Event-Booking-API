from dependencies import get_session
from schemes.users import RegistrationData, LoginData
from models.users import User

from fastapi import HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from pwdlib import PasswordHash

import jwt
from jwt.exceptions import InvalidTokenError

from security.jwt import create_access_token, create_refresh_token

import os 
from dotenv import load_dotenv

load_dotenv() 

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

async def register(register_data: RegistrationData, session: AsyncSession):
    statement = await session.execute(select(User).where(or_(User.username == register_data.username, User.email == register_data.email)))
    user = statement.scalar_one_or_none() 

    if user is not None:
        raise HTTPException(status_code=409, detail='user with this username or email already in system')

    hash_pass = PasswordHash.recommended()
    hashed_password = hash_pass.hash(register_data.password)


    user = User(username=register_data.username, email=register_data.email, hashed_password=hashed_password)

    session.add(user)
    await session.commit() 
    await session.refresh(user)

    return {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }


async def login(login_data: LoginData, session: AsyncSession):
    statement = await session.execute(select(User).where(User.username == login_data.username))
    user = statement.scalar_one_or_none() 

    if not user:
        raise HTTPException(status_code=401, detail='Wrong username or password')

    hash_pass = PasswordHash.recommended() 

    if not hash_pass.verify(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Wrong username or password')

    tokens = {
        'refresh_token': create_refresh_token(user.id, user.refresh_token_version),
        'access_token': create_access_token(user.id)
    }

    return tokens 


async def refresh(session: AsyncSession, refresh_token: str | None):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail='Invalid Credentials')

    try:
        payload = jwt.decode(refresh_token, secret_key, algorithms=[algorithm])

        sub = payload.get('sub')
        token_type = payload.get('type')
        version = payload.get('version')

        if sub is None:
            raise HTTPException(status_code=401, detail='Invalid Credentials')
        if token_type is None:
            raise HTTPException(status_code=401, detail='Invalid Credentials')
        if version is None:
            raise HTTPException(status_code=401, detail='Invalid Credentials')

        if token_type != 'refresh':
            raise HTTPException(status_code=401, detail='Invalid Credentials')

        
        user_id = int(sub) 
        version = int(version)

        statement = await session.execute(select(User).where(User.id == user_id))
        user = statement.scalar_one_or_none() 

        if user is None:
            raise HTTPException(status_code=401, detail='Invalid Credentials')

        if version != user.refresh_token_version:
            raise HTTPException(status_code=401, detail='Invalid Credentials')


        access_token = create_access_token(user.id)

        return access_token

    except (InvalidTokenError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail='Invalid Credentials')


async def logout(session: AsyncSession, response: Response, refresh_token: str | None):

    response.delete_cookie(key='refresh_token')

    if refresh_token is None:
            return {
                    'message': 'Logout success'
                }

    try:
        payload = jwt.decode(refresh_token, secret_key, algorithms=[algorithm])

        sub = payload.get('sub')
        token_type = payload.get('type')
        version = payload.get('version')

        if sub is None or token_type != 'refresh' or version is None:
            return {
                    'message': 'Logout success'
                }

        
        user_id = int(sub) 
        version = int(version)

        statement = await session.execute(select(User).where(User.id == user_id))
        user = statement.scalar_one_or_none() 

        if user is None:
            return {
                    'message': 'Logout success'
                }

        if version == user.refresh_token_version:
            user.refresh_token_version += 1 
            await session.commit()

        return {
            'message': 'Logout success'
        }

    except (InvalidTokenError, TypeError, ValueError):
        return {
            'message': 'Logout success'
        }   