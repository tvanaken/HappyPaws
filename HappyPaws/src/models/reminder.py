from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, relationship
from .base import Base


class Reminder(Base):
    __tablename__ = "reminders"

    # Standard reminder fields
    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    title = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    recurrence = Column(String)
    
    user = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
            "recurrence": self.recurrence if self.recurrence else None,
        }
