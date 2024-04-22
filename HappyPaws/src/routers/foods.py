from app.models import Food, Breed
from app.routers.breeds import _get_breed
from app.utils import get_session
from sqlalchemy import select, Float, func
from sqlalchemy.sql.expression import cast, text
from typing import Optional
from pydantic import BaseModel, validator
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

router = APIRouter()

class FoodModel(BaseModel):
    id: int
    image_url: str
    site_url: str
    rating: float
    review_count: int
    type: str
    life_stage: str
    size_constraint: str
    name: str
    ingredients: str
    nutrient_crude_protein: str
    nutrient_crude_fat: str
    nutrient_crude_fiber: str
    nutrient_moisture: str
    nutrient_dietary_starch: str
    nutrient_sugars: str
    nutrient_epa: str
    nutrient_dha: str
    nutrient_calcium: str
    nutrient_ash: str
    nutrient_l_carnitine: str
    nutrient_bacillus_coagulants: str
    nutrient_taurine: str
    nutrient_beta_carontene: str
    nutrient_phosphorous: str
    nutrient_niacin: str
    nutrient_chondroitin_sulfate: str
    nutrient_pyridoxine_vitamin_b6: str
    nutrient_vitamin_a: str
    nutrient_vitamin_e: str
    nutrient_ascorbic_acid: str
    nutrient_omega_6: str
    nutrient_omega_3: str
    nutrient_glucosamine: str
    nutrient_zinc: str
    nutrient_selenium: str
    nutrient_microorganisms: str
    nutrient_total_microorganisms: str

    class Config:
        orm_mode = True

@router.get("/api/foods", response_model=list[FoodModel])
async def get_foods():
    query = select(Food)
    session = await get_session()
    foods = await session.scalars(query)
    return foods


@router.post("/api/food")
async def create_food(food: dict):
    session = await get_session()

    food = Food(
        type=food.get("type"),
        life_stage=food.get("life_stage"),
        size_constraint=food.get("size_constraint"),
        name=food.get("name"),
        image_url=food.get("image_url"),
        site_url=food.get("site_url"),
        rating=food.get("rating"),
        review_count=food.get("review_count"),
        ingredients=food.get("ingredients"),
        nutrient_crude_protein=food.get("crude_protein"),
        nutrient_crude_fat=food.get("crude_fat")
        or food.get("fat_content"),
        nutrient_crude_fiber=food.get("crude_fiber"),
        nutrient_moisture=food.get("moisture"),
        nutrient_dietary_starch=food.get("dietary_starch"),
        nutrient_sugars=food.get("sugars"),
        nutrient_epa=food.get("epa")
        or food.get("eicosapentaenoic_acid_epa")
        or food.get("epa_eicosapentaenoic_acid"),
        nutrient_dha=food.get("dha")
        or food.get("docosahexaenoic_acid")
        or food.get("docosahexaenoic_acid_dha")
        or food.get("dha_docosahexaenoic_acid"),
        nutrient_calcium=food.get("calcium"),
        nutrient_ash=food.get("ash"),
        nutrient_l_carnitine=food.get("l_carnitine"),
        nutrient_bacillus_coagulants=food.get("bacillus_coagulants")
        or food.get("bacillus_coagulans"),
        nutrient_taurine=food.get("taurine"),
        nutrient_beta_carontene=food.get("beta_carontene"),
        nutrient_phosphorous=food.get("phosphorous") or food.get("phosphorus"),
        nutrient_niacin=food.get("niacin"),
        nutrient_chondroitin_sulfate=food.get("chondroitin_sulfate"),
        nutrient_pyridoxine_vitamin_b6=food.get("pyridoxine_vitamin_b6"),
        nutrient_vitamin_a=food.get("vitamin_a"),
        nutrient_vitamin_e=food.get("vitamin_e"),
        nutrient_ascorbic_acid=food.get("ascorbic_acid") or food.get("ascorbic_acid_vitamin_c"),
        nutrient_omega_6=food.get("omega_6") or food.get("omega_6_fatty_acids"),
        nutrient_omega_3=food.get("omega_3") or food.get("omega_3_fatty_acids"),
        nutrient_glucosamine=food.get("glucosamine") or food.get("glucoasmine"),
        nutrient_zinc=food.get("zinc"),
        nutrient_selenium=food.get("selenium"),
        nutrient_microorganisms=food.get("microorganisms"),
        nutrient_total_microorganisms=food.get("total_microorganisms")
        or food.get("total_lactic_acid_microorganisms"),
    )
    session.add(food)
    await session.commit()

    return JSONResponse(content=food.to_dict(), status_code=201)

NUTRIENT_THRESHOLDS = {
    "puppy": {"Low Activity": (30, 10), "Moderately Active": (32, 14), "High Activity": (35, 18)},
    "adult": {"Low Activity": (25, 12), "Moderately Active": (28, 15), "High Activity": (30, 20)},
    "senior": {"Low Activity": (20, 10), "Moderately Active": (22, 12), "High Activity": (25, 15)}
}

@router.get("/api/recommended_foods", response_model=list[FoodModel])
async def get_recommended_foods(breedId: int, age: int, activityLevel: str, session: AsyncSession = Depends(get_session)):
    breed_result = await session.execute(select(Breed).where(Breed.id == breedId))
    breed = breed_result.scalars().first()
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")
    
    life_stage = determine_life_stage(breed.size, age)
    protein_min, fat_min = NUTRIENT_THRESHOLDS[life_stage][activityLevel]

    query = select(Food).where(
        (Food.size_constraint == breed.size) | (Food.size_constraint == "any"),
        Food.life_stage == life_stage,
        cast(func.replace(Food.nutrient_crude_protein, '%', ''), Float) >= protein_min,
        cast(func.replace(Food.nutrient_crude_fat, '%', ''), Float) >= fat_min,
    ).order_by(Food.rating.desc(), Food.review_count.desc()).limit(5)

    food_results = await session.execute(query)
    foods = food_results.scalars().all()

    if not foods:
        raise HTTPException(status_code=404, detail="No suitable foods found")
    
    return foods

def determine_life_stage(size, age):
    if age <= 1:
        return "puppy"
    elif size == "large" and age >= 7:
        return "senior"
    elif size != "large" and age >= 10:
        return "senior"
    else:
        return "adult"