from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True) 
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

pets = relationship("Pet", back_populates="user", cascade="all, delete")