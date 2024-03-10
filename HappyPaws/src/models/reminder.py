from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, DateTime, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .base import Base


class Reminder(Base):
    __tablename__ = "reminders"

    # Standard reminder fields
    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    title = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    # Recurring reminder fields
    # startTime = Column(DateTime)
    # endTime = Column(DateTime)
    # startRecur = Column(Date)
    # endRecur = Column(Date)
    # daysOfWeek = Column(ARRAY(Integer))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
            # "startTime": self.startTime.isoformat() if self.startTime else None,
            # "endTime": self.endTime.isoformat() if self.endTime else None,
            # "startRecur": self.startRecur.isoformat() if self.startRecur else None,
            # "endRecur": self.endRecur.isoformat() if self.endRecur else None,
            # "daysOfWeek": self.daysOfWeek
        }