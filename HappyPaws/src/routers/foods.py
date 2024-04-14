from app.models import Food, Breed
from app.routers.breeds import _get_breed
from app.utils import get_session
from sqlalchemy import select, Float
from sqlalchemy.sql.expression import cast, text
import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

PROTEIN_THRESHOLDS = {"Puppy": 28, "adult": 25, "senior": 20}
FAT_THRESHOLDS = {"Low Activity": 12, "Moderately Active": 15, "High Activity": 20}

@router.get("/api/foods")
async def get_foods():
    query = select(Food)
    session = await get_session()
    foods = await session.scalars(query)
    return JSONResponse(content=[food.to_dict() for food in foods], status_code=200)


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

@router.get("/api/recommended_foods")
async def get_recommended_foods(breedId: int, age: int, activityLevel: str):
    session = await get_session()
    breed = await _get_breed(breedId)
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")
    
    life_stage = determine_life_stage(breed.size, age)

    protein_min = PROTEIN_THRESHOLDS[life_stage]
    fat_min = FAT_THRESHOLDS[activityLevel]

    query = select(Food).where(
        (Food.size_constraint == breed.size) | (Food.size_constraint == "any"),
        Food.life_stage == life_stage,
        cast(text("REPLACE(Food.nutrient_crude_protein, '%', '')"), Float) >= protein_min,
        cast(text("REPLACE(Food.nutrient_crude_fat, '%', '')"), Float) >= fat_min,
    ).order_by(Food.rating.desc(), Food.review_count.desc()).limit(5)

    food_results = await session.execute(query)
    foods = food_results.scalars().all()

    if not foods:
        raise HTTPException(status_code=404, detail="No suitable foods found")
            
    return JSONResponse(content=[food.to_dict() for food in foods], status_code=200)

def determine_life_stage(size, age):
    if age <= 1:
        return "puppy"
    elif size == "large" and age >= 7:
        return "senior"
    elif size != "large" and age >= 10:
        return "senior"
    else:
        return "adult"