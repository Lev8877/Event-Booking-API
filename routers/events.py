from schemes.events import GetEventsResponse, EventData, PostEvent, PatchEvent

from services.events import get_events, get_event, post_event, patch_event, delete_event

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_session, get_current_admin

from models.users import User

router = APIRouter() 

@router.get('/events', response_model=GetEventsResponse)
async def get_events_router(session: AsyncSession = Depends(get_session), limit: int | None = None, offset: int | None = None, search: str | None = None, status: str | None = None):
    return await get_events(session=session, limit=limit, offset=offset, search=search, status=status)


@router.get('/events/{event_id}', response_model=EventData)
async def get_event_router(event_id: int, session: AsyncSession = Depends(get_session)):
    return await get_event(session=session, event_id=event_id)


@router.post('/events', response_model=EventData)
async def post_event_router(event_data: PostEvent, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_admin)):
    return await post_event(session=session, event_data=event_data)


@router.patch('/events/{event_id}', response_model=EventData)
async def patch_event_router(event_id: int, event_data: PatchEvent, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_admin)):
    return await patch_event(session=session, event_data=event_data, event_id=event_id)


@router.delete('/events/{event_id}')
async def delete_event_router(event_id: int, user: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    return await delete_event(session=session, event_id=event_id)