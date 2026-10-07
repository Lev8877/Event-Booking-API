from typing import TYPE_CHECKING

from database import Base 

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from datetime import datetime

if TYPE_CHECKING:
    from models.bookings import Booking


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="user")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    refresh_token_version: Mapped[int] = mapped_column(default=0)

    bookings: Mapped[list['Booking']] = relationship(back_populates='user')
    

