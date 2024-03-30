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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "weights": self.weights,
            "breed_description": self.breed_description,
            "health_description": self.health_description,
            "groom_description": self.groom_description,
            "nutrition_description": self.nutrition_description,
        }
