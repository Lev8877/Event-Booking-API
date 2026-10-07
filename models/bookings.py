from typing import TYPE_CHECKING

from database import Base 

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, UniqueConstraint

from datetime import datetime



if TYPE_CHECKING:
    from models.users import User
    from models.events import Event


class Booking(Base):
    __tablename__ = 'bookings'

    __table_args__ = (UniqueConstraint('user_id','event_id'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id')) 
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


    user: Mapped['User'] = relationship(back_populates='bookings')
    event: Mapped['Event'] = relationship(back_populates='bookings')