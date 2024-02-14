from app.utils import get_current_user, get_session
from app.models import User
from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.pet import Pet
from routers import pets

router = APIRouter()


def _validate_user(user: dict):
    if user.get("username") is None:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    if user.get("email") is None:
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    if user.get("password") is None:
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    return user


async def _get_user(user_id: int):
    session = await get_session()
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/users")
async def get_user():
    user = await get_current_user()
    return JSONResponse(content=user.to_dict(), status_code=200)


@router.get("/api/users")
async def get_users():
    query = select(User)
    session = await get_session()
    users = await session.scalars(query)
    return JSONResponse(content=[user.to_dict() for user in users], status_code=200)


@router.get("/api/users/{user_id}")
async def get_user(user_id: int):
    user = await _get_user(user_id)
    if user:
        return user.to_dict()
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)


@router.post("/api/user")
async def create_user(user: dict):
    # user = await get_current_user()
    session = await get_session()
    user = _validate_user(user)

    user = User(
        username=user.get("username"),
        email=user.get("email"),
        password=user.get("password")
    )
    session.add(user)
    await session.commit()

    return JSONResponse(content=user.to_dict(), status_code=201)


# @router.delete("/api/user/{user_id}")
# async def delete_user(user_id: int):
#     user = await get_current_user()
#     session = await get_session()
#     if user_id == user.id:
#         user_pets_qeury = select(Pet).where(Pet.user_id == user.id)
#         user_pets = await session.scalars(user_pets_qeury)
#         for pet in user_pets:
#             await session.delete(pet)
#         await session.flush()
#         await session.delete(user)
#         await session.commit()
#         return JSONResponse(content={"message": "User deleted"}, status_code=200)
#     else:
#         return JSONResponse(content={"message": "Not authorized"}, status_code=401)