from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone


class PostCreate(BaseModel):
    title: str
    content: str
    breed_id: int
    user_id: int

class PostList(BaseModel):
    id: int
    title: str
    content: str
    breed_id: int
    user_id: int
    created_at: datetime


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    breed_id = Column(Integer, ForeignKey('breeds.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    breed = relationship("Breed", foreign_keys=[breed_id])
    user = relationship("User", foreign_keys=[user_id])
    comments = relationship("Comment", back_populates="post")