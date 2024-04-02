from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models import Comment, User, comment
from app.models.comment import CommentCreate, CommentRead
from app.models.login import get_current_user
from app.utils import get_session

router = APIRouter()

@router.post("/comments/", response_model=CommentRead)
async def create_comment(
     comment_data: CommentCreate, 
     session: AsyncSession = Depends(get_session), 
     current_user: User = Depends(get_current_user)
):
    new_comment = Comment(
    content=comment.content,
    user_id=current_user.id,
    post_id=comment.post_id
    )
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment

@router.get("/posts/{post_id}/comments/", response_model=List[CommentRead])
async def get_comments(post_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.execute(select(Comment).where(Comment.post_id == post_id))
        comments = result.scalars().all()
    return comments