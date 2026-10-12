from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from fastapi import HTTPException

from models.users import User
from models.events import Event
from models.bookings import Booking

from schemes.events import PostEvent, PatchEvent
from schemes.bookings import BookingResponse

from datetime import datetime

async def book_event(session: AsyncSession, event_id: int, user: User):
    statement = await session.execute(select(Event).where(Event.id == event_id))
    event = statement.scalar_one_or_none() 
    if event is None:
        raise HTTPException(status_code=404, detail='Event is not found')

    if event.date_and_time_of_event < datetime.now():
        raise HTTPException(status_code=409, detail='Event has already passed')

    statement = await session.execute(select(Booking).where(Booking.user_id == user.id, Booking.event_id == event_id))
    booking_check = statement.scalar_one_or_none() 
    if booking_check is not None:
        raise HTTPException(status_code=409, detail='You already booked this event')
    
    statement = await session.execute(select(func.count(Booking.id)).where(Booking.event_id == event_id))
    booking_count = statement.scalar_one()

    if event.max_participants <= booking_count:
        raise HTTPException(status_code=409, detail='This event reached max amout of participantians')
    

    booking = Booking(user_id=user.id, event_id=event_id)

    session.add(booking)
    await session.commit() 
    await session.refresh(booking)

    return {
        'id': booking.id,
        'event': event.title,
        'date_and_time': event.date_and_time_of_event
    }


async def get_my_events(session: AsyncSession, user: User):

    bookings_list = []

    statement = await session.execute(select(Booking).options(selectinload(Booking.event)).where(Booking.user_id == user.id))
    bookings = statement.scalars().all()

    for booking in bookings:
        bookings_list.append({
            'id': booking.id,
            'event': booking.event.title,
            'date_and_time': booking.event.date_and_time_of_event
        })

    return {
        'bookings': bookings_list
    }


async def delete_event(session: AsyncSession, booking_id: int, user: User):
    statement = await session.execute(select(Booking).where(Booking.id == booking_id))
    booking = statement.scalar_one_or_none() 
    if booking is None:
        raise HTTPException(status_code=404, detail='Booking has not been found')

    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')

    await session.delete(booking)
    await session.commit()

    return {
        'message': 'Booking has been deleted successfuly'
    }

