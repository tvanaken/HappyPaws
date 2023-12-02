from datetime import date
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, Text
from sqlalchemy.orm import mapped_column, relationship
from .base import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    type = Column(String)
    frequency = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "frequency": self.frequency,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None
        }