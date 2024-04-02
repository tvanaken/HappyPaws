from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from datetime import datetime, timezone


class CommentCreate(BaseModel):
    content: str
    post_id: int
    user_id: int

class CommentRead(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime | None = None
        

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')