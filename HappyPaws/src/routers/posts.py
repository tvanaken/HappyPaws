from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models import Post
from app.models.post import PostCreate, PostList
from app.utils import get_session
from app.models.login import get_current_user


router = APIRouter()


@router.get("/forum/posts", response_model=List[PostList])
async def list_forum_posts(session: AsyncSession = Depends(get_session)):
    async with session() as async_session:
        result = await async_session.execute(select(Post))
        posts = result.scalars().all()
        return posts

@router.post("/forum/posts", response_model=PostList)
async def create_forum_post(post: PostCreate, session: AsyncSession = Depends(get_session)):
    async with session() as async_session:
        new_post = Post(**post.dict())
        async_session.add(new_post)
        await async_session.commit()
        return new_post