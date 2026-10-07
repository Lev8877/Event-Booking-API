from typing import TYPE_CHECKING

from database import Base 

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from datetime import datetime



if TYPE_CHECKING:
    from models.bookings import Booking


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column() 
    address: Mapped[str] = mapped_column()
    date_and_time_of_event: Mapped[datetime] = mapped_column()
    max_participants: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    bookings: Mapped[list['Booking']] = relationship('event')