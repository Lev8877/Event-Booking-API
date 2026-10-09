from fastapi import FastAPI

from routers.users import router as users_router
from routers.events import router as event_router

from models.users import User
from models.events import Event
from models.bookings import Booking

app = FastAPI() 

app.include_router(users_router)
app.include_router(event_router)

