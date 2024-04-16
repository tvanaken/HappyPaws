from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from app.routers.users import oauth2_scheme
from app.routers.breeds import _get_breed_name
from app.models import Post, Breed
from app.utils import get_session
from app.models.login import get_current_user
from pydantic import BaseModel



router = APIRouter()

class PostCreate(BaseModel):
    title: str
    content: str
    breed_name: str
    created_at: datetime


async def get_breed_id_by_name(session, breed_name):
    breed_id = await session.execute(select(Breed.id).where(Breed.name == breed_name))
    return breed_id.scalar_one_or_none()


@router.get("/forum/posts")
async def list_forum_posts(session: AsyncSession = Depends(get_session)):
    session = await get_session()
    query = select(Post)
    posts = await session.execute(query)
    return posts.scalars().all()

@router.post("/forum/posts", response_model=PostCreate)
async def create_post(
    post_data: PostCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    user = await get_current_user(token, session)

    post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=user.id,
        breed_name=post_data.breed_name,
        breed_id=await get_breed_id_by_name(session, post_data.breed_name),
        created_at=post_data.created_at
    )
    session.add(post)
    await session.commit()

    return JSONResponse(status_code=201, content={"message": "Post created successfully"})

    