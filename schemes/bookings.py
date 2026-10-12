from pydantic import BaseModel, ConfigDict

from datetime import datetime


class BookingResponse(BaseModel):
    id: int 
    event: str 
    date_and_time: datetime


class BookingsResponse(BaseModel):
    bookings: list[BookingResponse]