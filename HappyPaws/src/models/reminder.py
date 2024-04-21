from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSON
from .base import Base

class ReminderCreate(BaseModel):
    title: str
    start: datetime
    end: Optional[datetime] = None
    daysOfWeek: Optional[List[int]] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    startRecur: Optional[datetime] = None
    endRecur: Optional[datetime] = None
    color: Optional[str] = None

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)
    daysOfWeek = Column(JSON)
    startTime = Column(String, nullable=True)
    endTime = Column(String, nullable=True)
    startRecur = Column(DateTime, nullable=True)
    endRecur = Column(DateTime, nullable=True)
    color = Column(String, nullable=True)
    
    user = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
            "daysOfWeek": self.daysOfWeek,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "startRecur": self.startRecur.isoformat() if self.startRecur else None,
            "endRecur": self.endRecur.isoformat() if self.endRecur else None,
            "color": self.color,
        }
