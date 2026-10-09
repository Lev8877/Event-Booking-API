from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.events import Event

from fastapi import HTTPException

from models.users import User

from schemes.events import PostEvent, PatchEvent

from datetime import datetime

async def get_events(session: AsyncSession, limit: int | None, offset: int | None, search: str | None, status: str | None):
    statement = select(Event)

    if search is not None:
        statement = statement.where(Event.title.ilike(f'%{search}%'))
    if status is not None:
        if status == 'past':
            statement = statement.where(Event.date_and_time_of_event < datetime.now())
        elif status == 'future':
            statement = statement.where(Event.date_and_time_of_event > datetime.now())
        else:
            raise HTTPException(status_code=422, detail='Please enter: "past" or "future" if status parameter')

    
    statement = statement.order_by(Event.id)

    if limit is not None:
        statement = statement.limit(limit)
    if offset is not None:
        statement = statement.offset(offset)
    

    result = await session.execute(statement)
    events = result.scalars().all() 

    return {
        'events': events 
    }


async def get_event(session: AsyncSession, event_id: int):
    statement = await session.execute(select(Event).where(Event.id == event_id))
    event = statement.scalar_one_or_none() 

    if event is None:
        raise HTTPException(status_code=404, detail="Resource is not found")

    return event

async def post_event(session: AsyncSession, event_data: PostEvent):
    if len(event_data.title.strip()) == 0:
        raise HTTPException(status_code=422, detail="Empty title")
    if event_data.max_participants <= 0:
        raise HTTPException(status_code=422, detail="Wrong max participants")
    if event_data.date_and_time_of_event <= datetime.now():
        raise HTTPException(status_code=422, detail="Wrong date and/or time ")
    event = Event(title=event_data.title, description=event_data.description, address=event_data.address, date_and_time_of_event=event_data.date_and_time_of_event, max_participants=event_data.max_participants)

    session.add(event)
    await session.commit() 
    await session.refresh(event)

    return event 


async def patch_event(session: AsyncSession, event_data: PatchEvent, event_id):
    statement = await session.execute(select(Event).where(Event.id == event_id))
    event = statement.scalar_one_or_none() 
    if event is None:
        raise HTTPException(status_code=404, detail="This event doesnt exists")

    data = event_data.model_dump(exclude_unset=True)

    if "title" in data:
        if data["title"] is None or not data["title"].strip():
            raise HTTPException(status_code=422, detail='Empty title')

    if "max_participants" in data:
        if data["max_participants"] is None or data['max_participants'] <= 0:
            raise HTTPException(status_code=422, detail='Wrong max participants')

    if "date_and_time_of_event" in data:
        if (data['date_and_time_of_event'] is None or data['date_and_time_of_event'] <= datetime.now()):
            raise HTTPException(status_code=422, detail='Wrong date and/or time')

    for key, value in data.items():
        setattr(event, key, value)

    await session.commit() 
    await session.refresh(event)

    return event  


async def delete_event(session: AsyncSession, event_id: int):
    statement = await session.execute(select(Event).where(Event.id == event_id))
    event = statement.scalar_one_or_none() 
    if event is None:
        raise HTTPException(status_code=404, detail="This event doesnt exists")

    await session.delete(event)
    await session.commit() 

    return {
        'message': 'Event has been deleted successfuly'
    }