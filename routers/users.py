from services.users import login, register, refresh, logout
from schemes.users import RegistrationData, LoginData
from dependencies import get_session, get_current_user

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from models.users import User

router = APIRouter() 

@router.post('/register')
async def register_router(register_data: RegistrationData, session: AsyncSession = Depends(get_session)):
    return await register(register_data=register_data, session=session)


@router.post('/login')
async def login_router(response: Response, login_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    tokens = await login(login_data=login_data, session=session)

    response.set_cookie(key='refresh_token', value=tokens['refresh_token'], httponly=True, secure=False, samesite="lax")

    return {
        'access_token': tokens['access_token'],
        'token_type': 'bearer'
    }


@router.get('/me')
async def get_me(user: User = Depends(get_current_user)):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }


@router.post('/refresh')
async def refresh_router(refresh_token: str | None = Cookie(default=None), session: AsyncSession = Depends(get_session)):
    return await refresh(session=session, refresh_token=refresh_token)


@router.post('/logout')
async def logout_router(response: Response, refresh_token: str | None = Cookie(default=None), session: AsyncSession = Depends(get_session)):
    return await logout(session=session, response=response, refresh_token=refresh_token)