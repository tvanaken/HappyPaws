from sqlalchemy import Column, Integer, String, Numeric
from .base import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    ingredients = Column(String)
    crude_protein = Column(Numeric(precision=5, scale=2))
    crude_fat = Column(Numeric(precision=5, scale=2))
    crude_fiber = Column(Numeric(precision=5, scale=2))
    moisture = Column(Numeric(precision=5, scale=2))
    dietary_starch = Column(Numeric(precision=5, scale=2))
    epa = Column(Numeric(precision=5, scale=2))
    calcium = Column(Numeric(precision=5, scale=2))
    phosphorus = Column(Numeric(precision=5, scale=2))
    vitamin_e = Column(Integer)
    omega_6 = Column(Numeric(precision=5, scale=2))
    omega_3 = Column(Numeric(precision=5, scale=2))
    glucosamine = Column(Integer)
    microorganisms = Column(Integer)

    def to_dict(self):
        return{
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "ingredients": self.ingredients,
            "crude_protein": str(self.crude_protein),
            "crude_fat": str(self.crude_fat),
            "crude_fiber": str(self.crude_fiber),
            "moisture": str(self.moisture),
            "dietary_starch": str(self.dietary_starch),
            "epa": str(self.epa),
            "calcium": str(self.calcium),
            "phosphorus": str(self.phosphorus),
            "vitamin_e": self.vitamin_e,
            "omega_6": str(self.omega_6),
            "omega_3": str(self.omega_3),
            "glucosamine": self.glucosamine,
            "microorganisms": self.microorganisms
        }
