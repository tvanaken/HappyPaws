from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import mapped_column, relationship

from .base import Base


class Pet(Base):
    """
    Represents a pet.

    Attributes:
        id (int): The unique identifier of the pet.
        user_id (int): The ID of the user who owns the pet.
        breed_id1 (int): The ID of the primary breed of the pet.
        breed_id2 (int): The ID of the secondary breed of the pet.
        name (str): The name of the pet.
        weight (Decimal): The weight of the pet.
        birthday (datetime.date): The birthday of the pet.
        age (int): The age of the pet in years.
        bio (str): The biography or description of the pet.
        image_url (str): The URL of the pet's image.
        activity_level (str): The activity level of the pet.

    Methods:
        age_calc(): Calculates the age of the pet based on its birthday.
        to_dict(): Converts the pet object to a dictionary.

    """
    ...
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    breed_id1 = Column(Integer, ForeignKey("breeds.id"))
    breed1 = relationship("Breed", foreign_keys=[breed_id1])
    breed_id2 = Column(Integer, ForeignKey("breeds.id"))
    breed2 = relationship("Breed", foreign_keys=[breed_id2], post_update=True)
    name = Column(String)
    weight = Column(Numeric(precision=5, scale=2))
    birthday = Column(Date)
    age = Column(Integer)
    bio = Column(String)
    image_url = Column(String)
    activity_level = Column(String)

    def age_calc(self):
        today = date.today()
        if self.birthday:
            return (
                today.year
                - self.birthday.year
                - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            )
        else:
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "breed_id1": self.breed_id1,
            "breed_id2": self.breed_id2,
            "name": self.name,
            "weight": str(self.weight),
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "age": self.age_calc() if self.birthday else None,
            "bio": self.bio,
            "image_url": self.image_url,
            "activity_level": self.activity_level,
        }
