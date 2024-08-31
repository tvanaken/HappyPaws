from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone


class Post(Base):
    """
    Represents a post in the application.
    Attributes:
        id (int): The unique identifier of the post.
        title (str): The title of the post.
        content (str): The content of the post.
        breed_name (str): The name of the breed associated with the post.
        breed_id (int): The foreign key referencing the breed associated with the post.
        user_id (int): The foreign key referencing the user who created the post.
        created_at (datetime): The date and time when the post was created.
        breed (Breed): The breed associated with the post.
        user (User): The user who created the post.
        comments (List[Comment]): The comments associated with the post.
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    breed_name = Column(String)
    breed_id = Column(Integer, ForeignKey('breeds.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    breed = relationship("Breed", foreign_keys=[breed_id])
    user = relationship("User", foreign_keys=[user_id])
    comments = relationship("Comment", back_populates="post")