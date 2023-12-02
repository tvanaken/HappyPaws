import pytest
import pytest_asyncio
from app import server, utils
from app.db import DBManager, DBManagerAsync
from app.models import Base, User
from httpx import AsyncClient

DB_NAME_TEST = "test_pet_parent"


def create_database_and_tables():
    print("\ncreating tables...")
    DBManager.create_db_if_does_not_exist(db_name=DB_NAME_TEST)
    db_manager = DBManager(db_name=DB_NAME_TEST)
    engine = db_manager.get_engine()
    session = db_manager.get_session()
    Base.metadata.create_all(bind=engine)
    session.close()
    engine.dispose()


def drop_tables_and_database():
    print("\ndropping tables...")
    db_manager = DBManager(db_name=DB_NAME_TEST)
    engine = db_manager.get_engine()
    session = db_manager.get_session()
    Base.metadata.drop_all(bind=engine)
    DBManager.drop_db_if_exists(db_name=DB_NAME_TEST)
    session.close()
    engine.dispose()


@pytest_asyncio.fixture()
async def setup_teardown_testdb():
    create_database_and_tables()

    yield

    # close the async session:
    session = await utils.get_session()
    await session.close()

    drop_tables_and_database()


@pytest_asyncio.fixture()
def override_class_variables():
    utils.db_manager = DBManagerAsync(db_name=DB_NAME_TEST)


@pytest_asyncio.fixture()
async def create_fake_user():
    # create fake logged in user
    session = await utils.get_session()
    user = User(
        username="logged_in_user",
        first_name="Jane",
        last_name="Doe",
        email="jane_doe@yahoo.com",
    )
    session.add(user)
    await session.commit()


@pytest_asyncio.fixture(autouse=True)
async def testing_setup_teardown(
    setup_teardown_testdb, override_class_variables, create_fake_user
):
    # This fixture is run on every test
    # LIFO: runs setup_teardown_testdb, then override_class_variables
    # then create_fake_user
    pass


@pytest.fixture()
def get_client():
    return AsyncClient(
        app=server.app,
        base_url="http://localhost",
        headers={"Content-Type": "application/json"},
    )


@pytest_asyncio.fixture()
async def create_fake_users():
    fake_user_json = [
        {
            "username": "jennifer_anderson",
            "first_name": "Jennifer",
            "last_name": "Anderson",
            "email": "jennifer_anderson@yahoo.com",
        },
        {
            "username": "benjamin_davis",
            "first_name": "Benjamin",
            "last_name": "Davis",
            "email": "benjamin_davis@yahoo.com",
        },
        {
            "username": "katie_sullivan",
            "first_name": "Katie",
            "last_name": "Sullivan",
            "email": "katie_sullivan@hotmail.com",
        },
    ]
    session = await utils.get_session()
    users = []
    for user in fake_user_json:
        user = User(**user)
        session.add(user)
        users.append(user)
    await session.commit()
    return users
