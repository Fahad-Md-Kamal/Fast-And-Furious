import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient
from chapter6.mongodb.app import app, get_database
from chapter6.mongodb.models import PostDB

motor_client = AsyncIOMotorClient('mongodb://localhost:27017')
database_test = motor_client['chapter9_db_test']

def get_test_database():
    return database_test


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    app.dependency_overrides[get_database] = get_test_database
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url='http://app.io') as test_client:
            yield test_client

@pytest_asyncio.fixture(autouse=True, scope='module')
async def initial_posts():
    initial_posts = [
        PostDB(title='Post 1', content='Content 1'),
        PostDB(title='Post 2', content='Content 2'),
        PostDB(title='Post 3', content='Content 3'),
    ]
    await database_test["posts"].insert_many(
        [post.dict(by_allias=True) for post in initial_posts]
    )

    yield initial_posts

    await motor_client.drop_database('chapter9_db_test')