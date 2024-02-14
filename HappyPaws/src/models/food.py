from sqlalchemy import Column, Integer, String, Numeric
from .base import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    ingredients = Column(String)
    crude_protein = Column(String)
    crude_fat = Column(String)
    crude_fiber = Column(String)
    moisture = Column(String)
    dietary_starch = Column(String)
    sugars = Column(String)
    epa = Column(String)
    dha = Column(String)
    calcium = Column(String)
    ash = Column(String)
    l_carnitine = Column(String)
    bacillus_coagulants = Column(String)
    taurine = Column(String)
    beta_carontene = Column(String)
    phosphorous = Column(String)
    niacin = Column(String)
    chondroitin_sulfate = Column(String)
    pyridoxine_vitamin_b6 = Column(String)
    vitamin_a = Column(String)
    vitamin_e = Column(String)
    ascorbic_acid = Column(String)
    omega_6 = Column(String)
    omega_3 = Column(String)
    glucosamine = Column(String)
    zinc = Column(String)
    selenium = Column(String)
    microorganisms = Column(String)
    total_microorganisms = Column(String)

    def to_dict(self):
        return{
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "ingredients": self.ingredients,
            "crude_protein": str(self.crude_protein),
            "crude_fat": str(self.crude_fat),
            "crude_fiber": str(self.crude_fiber),
            "moisture": self.moisture,
            "dietary_starch": str(self.dietary_starch),
            "epa": str(self.epa),
            "dha": str(self.dha),
            "calcium": str(self.calcium),
            "ash": str(self.ash),
            "phosphorous": str(self.phosphorous),
            "niacin": self.niacin,
            "chondroitin_sulfate": self.chondroitin_sulfate,
            "pyridoxine_vitamin_b6": self.pyridoxine_vitamin_b6,
            "vitamin_a": self.vitamin_a,
            "vitamin_e": self.vitamin_e,
            "ascorbic_acid": self.ascorbic_acid,
            "omega_6": str(self.omega_6),
            "omega_3": str(self.omega_3),
            "glucosamine": self.glucosamine,
            "zinc": self.zinc,
            "selenium": self.selenium,
            "microorganisms": self.microorganisms,
            "total_microorganisms": self.total_microorganisms
        }
