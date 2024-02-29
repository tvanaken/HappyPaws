from datetime import datetime, timedelta
from typing import Annotated, Optional
from app.db import DBManagerAsync
from app.models import User
from sqlalchemy import select


_user = None
db_manager = DBManagerAsync()


async def get_session():
    """
    Session is cached in the db_manager (reuses the same session over and over)
    """
    return await db_manager.get_session()


# async def get_current_user():
#     """
#     Note that user is cached in _user global variable
#     """
#     global _user
#     user_id = 1
#     if _user is None:
#         print(f"querying database for user={user_id}...")
#         session = await get_session()
#         query = select(User).where(User.id == user_id)
#         result = await session.execute(query)
#         record = result.fetchone()
#         if record:
#             _user = record[0]
#         else:
#             raise Exception(f"No User in database with id={user_id}")
#     return _user

