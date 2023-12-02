import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy_utils.functions import database_exists


class DBManager:
    """
    Handles synchronous DB connections
    """

    def __init__(self, db_name=None):
        self.db_name = db_name
        self.engine = None
        self.session = None

    def get_connection_url(self):
        load_dotenv()
        db_name = self.db_name or os.environ.get("DB_NAME")
        return URL.create(
            drivername="postgresql",
            username=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=db_name,
        )

    def get_engine(self):
        if self.engine is None:
            url = self.get_connection_url()
            self.engine = create_engine(url)
        return self.engine

    def get_session(self):
        if not self.session:
            # print('Generating sync session...')
            Session = sessionmaker(self.get_engine())
            self.session = Session()
            self.session.begin()
        return self.session

    def cleanup(self):
        if not self.session:
            return
        self.session.close()

    @classmethod
    def create_db_if_does_not_exist(cls, db_name=None):
        db_manager = DBManager(db_name=db_name)
        url = db_manager.get_connection_url()
        if not database_exists(url):
            # print('creating database:', url)
            create_database(url)

    @classmethod
    def drop_db_if_exists(cls, db_name=None):
        db_manager = DBManager(db_name=db_name)
        url = db_manager.get_connection_url()
        if database_exists(url):
            # print('dropping database:', url)
            drop_database(url)

    @classmethod
    def database_exists(cls, db_name=None):
        db_manager = DBManager(db_name=db_name)
        url = db_manager.get_connection_url()
        return database_exists(url)


class DBManagerAsync:
    """
    Handles asynchronous DB connections
    """

    def __init__(self, db_name=None):
        self.db_name = db_name
        self.engine = None
        self.session = None

    def get_connection_url(self):
        load_dotenv()
        db_name = self.db_name or os.environ.get("DB_NAME")
        return URL.create(
            drivername="postgresql+asyncpg",
            username=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=db_name,
        )

    def get_engine(self):
        if self.engine is None:
            url = self.get_connection_url()
            self.engine = create_async_engine(url)
        return self.engine

    async def get_session(self):
        if not self.session:
            # print('Generating async session...')
            Session = sessionmaker(
                self.get_engine(), class_=AsyncSession, expire_on_commit=False
            )
            self.session = Session()
            await self.session.begin()
        return self.session

    async def cleanup(self):
        if self.session is not None:
            await self.session.close()
