from sqlalchemy import Column, Integer, Numeric, String

from .base import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    site_url = Column(String)
    rating = Column(Numeric)
    review_count = Column(Integer)
    type = Column(String)
    life_stage = Column(String)
    size_constraint = Column(String)
    name = Column(String)
    ingredients = Column(String)
    nutrient_crude_protein = Column(String)
    nutrient_crude_fat = Column(String)
    nutrient_crude_fiber = Column(String)
    nutrient_moisture = Column(String)
    nutrient_dietary_starch = Column(String)
    nutrient_sugars = Column(String)
    nutrient_epa = Column(String)
    nutrient_dha = Column(String)
    nutrient_calcium = Column(String)
    nutrient_ash = Column(String)
    nutrient_l_carnitine = Column(String)
    nutrient_bacillus_coagulants = Column(String)
    nutrient_taurine = Column(String)
    nutrient_beta_carontene = Column(String)
    nutrient_phosphorous = Column(String)
    nutrient_niacin = Column(String)
    nutrient_chondroitin_sulfate = Column(String)
    nutrient_pyridoxine_vitamin_b6 = Column(String)
    nutrient_vitamin_a = Column(String)
    nutrient_vitamin_e = Column(String)
    nutrient_ascorbic_acid = Column(String)
    nutrient_omega_6 = Column(String)
    nutrient_omega_3 = Column(String)
    nutrient_glucosamine = Column(String)
    nutrient_zinc = Column(String)
    nutrient_selenium = Column(String)
    nutrient_microorganisms = Column(String)
    nutrient_total_microorganisms = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "site_url": self.site_url,
            "rating": self.rating,
            "review_count": self.review_count,
            "type": self.type,
            "life_stage": self.life_stage,
            "size_constraint": self.size_constraint,
            "name": self.name,
            "ingredients": self.ingredients,
            "nutrient_crude_protein": self.nutrient_crude_protein,
            "nutrient_crude_fat": self.nutrient_crude_fat,
            "nutrient_crude_fiber": self.nutrient_crude_fiber,
            "nutrient_moisture": self.nutrient_moisture,
            "nutrient_dietary_starch": self.nutrient_dietary_starch,
            "nutrient_sugars": self.nutrient_sugars,
            "nutrient_epa": self.nutrient_epa,
            "nutrient_dha": self.nutrient_dha,
            "nutrient_calcium": self.nutrient_calcium,
            "nutrient_ash": self.nutrient_ash,
            "nutrient_l_carnitine": self.nutrient_l_carnitine,
            "nutrient_bacillus_coagulants": self.nutrient_bacillus_coagulants,
            "nutrient_taurine": self.nutrient_taurine,
            "nutrient_beta_carontene": self.nutrient_beta_carontene,
            "nutrient_phosphorous": self.nutrient_phosphorous,
            "nutrient_niacin": self.nutrient_niacin,
            "nutrient_chondroitin_sulfate": self.nutrient_chondroitin_sulfate,
            "nutrient_pyridoxine_vitamin_b6": self.nutrient_pyridoxine_vitamin_b6,
            "nutrient_vitamin_a": self.nutrient_vitamin_a,
            "nutrient_vitamin_e": self.nutrient_vitamin_e,
            "nutrient_ascorbic_acid": self.nutrient_ascorbic_acid,
            "nutrient_omega_6": self.nutrient_omega_6,
            "nutrient_omega_3": self.nutrient_omega_3,
            "nutrient_glucosamine": self.nutrient_glucosamine,
            "nutrient_zinc": self.nutrient_zinc,
            "nutrient_selenium": self.nutrient_selenium,
            "nutrient_microorganisms": self.nutrient_microorganisms,
            "nutrient_total_microorganisms": self.nutrient_total_microorganisms,
        }
