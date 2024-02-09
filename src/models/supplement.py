from sqlalchemy import Column, Integer, String
from .base import Base


class Supplement(Base):
    __tablename__ = "supplements"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    lifestage = Column(String)
    ailment = Column(String)
    breed_size = Column(String)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "lifestage": self.lifestage,
            "ailment": self.ailment,
            "breed_size": self.breed_size,
        }
