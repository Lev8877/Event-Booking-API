from pydantic import BaseModel, ConfigDict

from datetime import datetime


class EventData(BaseModel):
    id: int
    title: str
    description: str
    address: str
    date_and_time_of_event: datetime
    max_participants: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GetEventsResponse(BaseModel):
    events: list[EventData] 


class PostEvent(BaseModel):
    title: str 
    description: str 
    address: str 
    date_and_time_of_event: datetime
    max_participants: int


class PatchEvent(BaseModel):
    title: str | None = None
    description: str | None = None 
    address: str | None = None 
    date_and_time_of_event: datetime | None = None 
    max_participants: int | None = None 