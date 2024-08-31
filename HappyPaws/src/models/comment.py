from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from datetime import datetime, timezone
        

class Comment(Base):
    """
    Represents a comment on a post.
    Attributes:
        id (int): The unique identifier of the comment.
        content (str): The content of the comment.
        user_id (int): The ID of the user who made the comment.
        post_id (int): The ID of the post the comment belongs to.
        created_at (datetime): The timestamp when the comment was created.
    Relationships:
        user (User): The user who made the comment.
        post (Post): The post the comment belongs to.
    Methods:
        to_dict(): Converts the comment object to a dictionary.
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }