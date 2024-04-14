from sqlalchemy import Column, Integer, String

from .base import Base


class Supplement(Base):
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
