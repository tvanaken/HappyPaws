from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, contains_eager, selectinload, aliased
from typing import List, Optional
from datetime import datetime
from app.routers.users import oauth2_scheme
from app.routers.breeds import _get_breed_name
from app.models import Post, Breed, Comment
from app.utils import get_session
from app.models.login import get_current_user
from pydantic import BaseModel



router = APIRouter()

class PostDetails(BaseModel):
    title: str
    content: str
    breed_name: str
    created_at: datetime
    user_id: int
    breed_id: int

class PostCreate(BaseModel):
    title: str
    content: str
    breed_name: str
    created_at: datetime


async def get_breed_id_by_name(session, breed_name):
    """
    Retrieves the breed ID based on the given breed name.

    Parameters:
    - session: The database session to use for the query.
    - breed_name: The name of the breed to search for.

    Returns:
    - The breed ID if found, otherwise None.
    """
    breed_id = await session.execute(select(Breed.id).where(Breed.name == breed_name))
    return breed_id.scalar_one_or_none()


@router.get("/forum/posts")
async def list_forum_posts(session: AsyncSession = Depends(get_session)):
    """
    Retrieve a list of forum posts.

    Parameters:
    - session: The database session to use (default: Depends(get_session))

    Returns:
    - A list of forum posts.
    """
    session = await get_session()
    query = select(Post).order_by(Post.created_at.desc())
    posts = await session.execute(query)
    return posts.scalars().all()


@router.get("/forum/posts/filtered")
async def get_posts_filtered(breed_name: Optional[str] = None, search: Optional[str] = None, session: AsyncSession = Depends(get_session)):
    """
    Retrieves filtered posts based on the provided breed name and search keyword.
    Parameters:
    - breed_name (Optional[str]): The breed name to filter the posts by.
    - search (Optional[str]): The keyword to search for in the post titles and content.
    - session (AsyncSession): The async session to use for executing the query.
    Returns:
    - List[Post]: A list of posts that match the filter criteria.
    """
    query = select(Post)
    if breed_name:
        query = query.where(Post.breed_name == breed_name)
    if search:
        query = query.where(Post.title.contains(search) | Post.content.contains(search))
    posts = await session.execute(query)
    return posts.scalars().all()


@router.get("/forum/posts/{post_id}")
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a post by its ID.
    Parameters:
    - post_id (int): The ID of the post to retrieve.
    - session (AsyncSession, optional): The database session to use. Defaults to the session obtained from `get_session` dependency.
    Returns:
    - Post: The retrieved post.
    """
    query = (
        select(Post)
        .where(Post.id == post_id)
    )
    
    post = await session.execute(query)
    return post.scalars().first()


@router.post("/forum/posts", response_model=PostCreate)
async def create_post(
    post_data: PostCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new post in the forum.
    Parameters:
    - post_data (PostCreate): The data for the new post.
    - token (str): The authentication token.
    - session (AsyncSession): The database session.
    Returns:
    - JSONResponse: The response indicating the success of the post creation.
    """
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

    