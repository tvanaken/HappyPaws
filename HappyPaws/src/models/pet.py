from datetime import date
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date
from sqlalchemy.orm import mapped_column, relationship
from .base import Base



class Pet(Base):
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
    bio = Column(String)

    def age(self):
        today = date.today()
        if self.birthday:
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        else:
            return None

    def to_dict(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "breed_id1": self.breed_id1,
            "breed_id2": self.breed_id2,
            "name": self.name,
            "weight": str(self.weight),
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "age": self.age() if self.birthday else None,
            "bio": self.bio
        }
