from app.models import Food
from app.utils import get_session
from sqlalchemy import select

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


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

@router.get("/api/recommended_foods?breedId=${breedId}&weight=${weight}&age=${age}&activityLevel=${activityLevel}")
async def get_recommended_foods(breedId: int, weight: int, age: int, activityLevel: str):

    return JSONResponse(content={"message": "Not implemented"}, status_code=501)