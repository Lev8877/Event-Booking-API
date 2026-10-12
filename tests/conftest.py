import pytest 
import asyncio

from main import app 

from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text

import os 
from dotenv import load_dotenv

from dependencies import get_session

from database import Base

from models.users import User
from models.events import Event
from models.bookings import Booking


load_dotenv() 

test_database_url = os.getenv('TEST_DATABASE_URL')
database_url = os.getenv('DATABASE_URL')

if not test_database_url:
    raise RuntimeError('TEST_DATABASE_URL is not configured')
if test_database_url == database_url:
    raise RuntimeError("Test database must differ from development database")

engine = create_async_engine(test_database_url, poolclass=NullPool)

TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture()
def client():
    app.dependency_overrides[get_session] = override_get_session

    try:
        with TestClient(app) as testclient:
            yield testclient
    finally:
        app.dependency_overrides.pop(get_session, None)


async def create_test_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
def prepare_test_database():
    asyncio.run(create_test_tables())


async def clear_test_data():
    async with engine.begin() as connection:
        await connection.execute(text('TRUNCATE TABLE events, users, bookings RESTART IDENTITY CASCADE'))


@pytest.fixture(autouse=True)
def clear_database(prepare_test_database):
    asyncio.run(clear_test_data())

    try:
        yield 
    finally:
        asyncio.run(clear_test_data())



    