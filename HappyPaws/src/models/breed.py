from sqlalchemy import Column, Integer, String
from .base import Base


class Breed(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    weights = Column(String)
    breed_description = Column(String)
    health_description = Column(String)
    groom_description = Column(String)
    nutrition_description = Column(String)
