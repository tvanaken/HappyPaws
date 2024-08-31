from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from app.models import Comment, User, comment
from app.routers.users import oauth2_scheme
from app.models.login import get_current_user
from app.utils import get_session
from pydantic import BaseModel

router = APIRouter()

class CommentCreate(BaseModel):
    """
    Represents a comment creation request.

    Attributes:
        content (str): The content of the comment.
        created_at (datetime): The timestamp when the comment was created.
    """
    content: str
    created_at: datetime


class CommentRead(BaseModel):
    """
    Represents a comment read model.

    Attributes:
        id (int): The unique identifier of the comment.
        content (str): The content of the comment.
        user_id (int): The user ID associated with the comment.
        post_id (int): The post ID associated with the comment.
        created_at (datetime): The timestamp when the comment was created.
    """
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime


@router.get("/forum/posts/{post_id}/comments")
async def list_post_comments(post_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a list of comments for a specific post.

    Parameters:
    - post_id (int): The ID of the post.
    - session (AsyncSession, optional): The database session. Defaults to Depends(get_session).

    Returns:
    - List[Comment]: A list of comments for the specified post.
    """
    query = select(Comment).where(Comment.post_id == post_id)
    comments = await session.execute(query)
    return comments.scalars().all()
    

@router.post("/forum/posts/{post_id}/comments", response_model=CommentCreate)
async def create_comment(post_id: int, comment_data: CommentCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    """
    Create a comment for a post.
    Parameters:
    - post_id (int): The ID of the post to create the comment for.
    - comment_data (CommentCreate): The data for the comment to be created.
    - token (str, optional): The authentication token. Defaults to Depends(oauth2_scheme).
    - session (AsyncSession, optional): The database session. Defaults to Depends(get_session).
    Returns:
    - JSONResponse: The JSON response containing the created comment data.
    Raises:
    - HTTPException: If the user is not authorized.
    """
    user = await get_current_user(token, session)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    comment = Comment(
        content=comment_data.content,
        post_id=post_id,
        user_id=user.id,
        created_at=comment_data.created_at
    )

    session.add(comment)
    await session.commit()

    return JSONResponse(content=comment.to_dict(), status_code=201)