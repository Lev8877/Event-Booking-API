from services.bookings import book_event, get_my_events, delete_event

from schemes.bookings import BookingResponse, BookingsResponse

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_session, get_current_admin, get_current_user

from models.users import User

router = APIRouter() 


@router.post('/events/{event_id}/bookings', response_model=BookingResponse)
async def book_event_router(event_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await book_event(session=session, event_id=event_id, user=user)


@router.get('/bookings', response_model=BookingsResponse)
async def get_my_events_router(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await get_my_events(session=session, user=user)

@router.delete('/bookings/{booking_id}')
async def delete_event_router(booking_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await delete_event(session=session, booking_id=booking_id, user=user)
