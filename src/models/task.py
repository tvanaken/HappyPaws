from app.models.base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    done = Column(Boolean, default=False)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
