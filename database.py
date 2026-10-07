import os 
from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase

load_dotenv() 

database_url = os.getenv("DATABASE_URL")


class Base(DeclarativeBase):
    pass 