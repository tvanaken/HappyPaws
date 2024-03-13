from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date
from sqlalchemy.orm import mapped_column, relationship
from .base import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    breed_id1 = mapped_column(Integer, ForeignKey("breeds.id"))
    breed = relationship("Breed")
    breed_id2 = mapped_column(Integer, ForeignKey("breeds.id"))
    breed = relationship("Breed")
    name = Column(String)
    weight = Column(Numeric(precision=5, scale=2))
    birthday = Column(Date)

    def to_dict(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "breed_id1": self.breed_id1,
            "breed_id2": self.breed_id2,
            "name": self.name,
            "weight": str(self.weight),
            "birthday": self.birthday.isoformat() if self.birthday else None
        }
