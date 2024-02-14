from sqlalchemy import Column, Integer, String
from .base import Base


class Breed(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    suggested_supplements = Column(String)
    suggested_exercise = Column(String)