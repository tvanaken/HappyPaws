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
    """
    Represents a reminder object with various properties.

    Attributes:
        title (str): The title of the reminder.
        start (datetime): The start date and time of the reminder.
        end (Optional[datetime], optional): The end date and time of the reminder. Defaults to None.
        daysOfWeek (Optional[List[int]], optional): The list of days of the week when the reminder occurs. Defaults to None.
        startTime (Optional[str], optional): The start time of the reminder. Defaults to None.
        endTime (Optional[str], optional): The end time of the reminder. Defaults to None.
        startRecur (Optional[datetime], optional): The start date and time of the recurring reminder. Defaults to None.
        endRecur (Optional[datetime], optional): The end date and time of the recurring reminder. Defaults to None.
        color (Optional[str], optional): The color of the reminder. Defaults to None.
    """
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
    """
    Represents a reminder.
    Attributes:
        id (int): The unique identifier of the reminder.
        user_id (int): The ID of the user associated with the reminder.
        title (str): The title of the reminder.
        start (datetime): The start date and time of the reminder.
        end (datetime): The end date and time of the reminder.
        daysOfWeek (list): The list of days of the week for recurring reminders.
        startTime (str): The start time of the reminder.
        endTime (str): The end time of the reminder.
        startRecur (datetime): The start date and time for recurring reminders.
        endRecur (datetime): The end date and time for recurring reminders.
        color (str): The color of the reminder.
    Methods:
        to_dict(): Converts the reminder object to a dictionary.
    """
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
