from sqlalchemy import Column, Integer, String

from .base import Base


class Supplement(Base):
    """
    Represents a supplement.

    Attributes:
        id (int): The unique identifier of the supplement.
        name (str): The name of the supplement.
        image_url (str): The URL of the supplement's image.
        site_url (str): The URL of the supplement's website.
        rating (str): The rating of the supplement.
        review_count (int): The number of reviews for the supplement.
        description (str): The description of the supplement.
        lifestage (str): The lifestage the supplement is suitable for.
        ailment (str): The ailment the supplement is intended to address.
        breed_size (str): The breed size the supplement is suitable for.

    Methods:
        to_dict(): Converts the supplement object to a dictionary.

    """
    ...
    __tablename__ = "supplements"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image_url = Column(String)
    site_url = Column(String)
    rating = Column(String)
    review_count = Column(Integer)
    description = Column(String)
    lifestage = Column(String)
    ailment = Column(String)
    breed_size = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
            "site_url": self.site_url,
            "rating": self.rating,
            "review_count": self.review_count,
            "description": self.description,
            "lifestage": self.lifestage,
            "ailment": self.ailment,
            "breed_size": self.breed_size,
        }
