from datetime import datetime, timedelta
from typing import Annotated, Optional
from app.utils import get_session
from app.models import User, UserCreate
from app.models.login import get_current_user, AccessToken
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.pet import Pet
from dotenv import load_dotenv
import os




router = APIRouter()
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str



async def _validate_user(user: dict):
    if user.get("email") is None:
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    if user.get("password") is None:
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    return user

async def authenticate_user(email: str, password: str, session: AsyncSession) -> Optional[User]:
    user = await get_user_by_email(email=email, session=session)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User]:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    record = result.fetchone()
    if record:
        user = record[0]
    else:
        return None
    return user

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def _get_user(user_id: int):
    session = await get_session()
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/users/me")
async def get_user_me(current_user: User = Depends(get_current_user)):
    user = await get_current_user()
    if user:
        return JSONResponse(content=user.to_dict(), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/api/users")
async def get_users():
    user = await get_current_user()

    if user.id == 2:
        query = select(User)
        session = await get_session()
        users = await session.scalars(query)
        return JSONResponse(content=[user.to_dict() for user in users], status_code=200)
    else:
        return JSONResponse(content={"message": "Not authorized"}, status_code=401)


@router.get("/api/users/{user_id}")
async def get_user(user_id: int):
    user = await _get_user(user_id)
    if user:
        return user.to_dict()
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)


@router.post("/api/users")
async def create_user(user_details: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(email=user_details.email, session=session)
    if user:
        return JSONResponse(content={"message": "User already exists"}, status_code=400)
    else:
        hashed_password = get_password_hash(user_details.password)
        user = User(
            email=user_details.email,
            password=hashed_password
        )

        session.add(user)
        await session.commit()

        return JSONResponse(content={"message": "User successfully created"}, status_code=201)


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

@router.post("/api/users/token")
async def login(login_request: LoginRequest, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(login_request.username, login_request.password, session)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}