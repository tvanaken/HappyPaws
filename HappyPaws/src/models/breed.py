from sqlalchemy import Column, Integer, String

from .base import Base



class Breed(Base):
    """
    Represents a breed of pet.

    Attributes:
        id (int): The unique identifier of the breed.
        name (str): The name of the breed.
        weights (str): The weight range of the breed.
        breed_description (str): The description of the breed.
        health_description (str): The health information of the breed.
        groom_description (str): The grooming information of the breed.
        nutrition_description (str): The nutrition information of the breed.
        max_weight (int): The maximum weight of the breed.
        size (str): The size category of the breed.

    Methods:
        to_dict(): Converts the breed object to a dictionary.

    """
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    weights = Column(String)
    breed_description = Column(String)
    health_description = Column(String)
    groom_description = Column(String)
    nutrition_description = Column(String)
    max_weight = Column(Integer)
    size = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "weights": self.weights,
            "breed_description": self.breed_description,
            "health_description": self.health_description,
            "groom_description": self.groom_description,
            "nutrition_description": self.nutrition_description,
            "max_weight": self.max_weight,
            "size": self.size,
        }
