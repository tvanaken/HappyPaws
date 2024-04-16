from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from app.models import Comment, User, comment
from app.routers.users import oauth2_scheme
from app.models.comment import CommentCreate, CommentRead
from app.models.login import get_current_user
from app.utils import get_session
from pydantic import BaseModel

router = APIRouter()

@router.post("/forum/posts/{post_id}/comments", response_model=CommentCreate)
async def create_comment(post_id: int, comment_data: CommentCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
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

    return JSONResponse(content={"message": "Comment created successfully"}, status_code=201)