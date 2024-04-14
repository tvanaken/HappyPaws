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
        name=food.get("name"),
        image_url=food.get("image_url"),
        site_url=food.get("site_url"),
        rating=food.get("rating"),
        review_count=food.get("review_count"),
        ingredients=food.get("ingredients"),
        crude_protein=food.get("crude_protein"),
        crude_fat=food.get("crude_fat")
        or food.get("fat_content"),
        crude_fiber=food.get("crude_fiber"),
        moisture=food.get("moisture"),
        dietary_starch=food.get("dietary_starch"),
        sugars=food.get("sugars"),
        epa=food.get("epa")
        or food.get("eicosapentaenoic_acid_epa")
        or food.get("epa_eicosapentaenoic_acid"),
        dha=food.get("dha")
        or food.get("docosahexaenoic_acid")
        or food.get("docosahexaenoic_acid_dha")
        or food.get("dha_docosahexaenoic_acid"),
        calcium=food.get("calcium"),
        ash=food.get("ash")
        or food.get("crude_ash"),
        l_carnitine=food.get("l_carnitine"),
        bacillus_coagulants=food.get("bacillus_coagulants")
        or food.get("bacillus_coagulans"),
        taurine=food.get("taurine"),
        beta_carontene=food.get("beta_carontene"),
        phosphorous=food.get("phosphorous") 
        or food.get("phosphorus"),
        niacin=food.get("niacin"),
        chondroitin_sulfate=food.get("chondroitin_sulfate")
        or food.get("chondroitin_sulphate"),
        pyridoxine_vitamin_b6=food.get("pyridoxine_vitamin_b6"),
        vitamin_a=food.get("vitamin_a"),
        vitamin_e=food.get("vitamin_e"),
        ascorbic_acid=food.get("ascorbic_acid") or food.get("ascorbic_acid_vitamin_c"),
        omega_6=food.get("omega_6") 
        or food.get("omega-6")
        or food.get("omega_6_fatty_acids")
        or food.get("linoleic_acid_omega_6_fatty_acid"),
        omega_3=food.get("omega_3") 
        or food.get("omega-3")
        or food.get("omega_3_fatty_acids")
        or food.get("alpha_linolenic_acid_omega_3_fatty_acid"),
        glucosamine=food.get("glucosamine") or food.get("glucoasmine"),
        zinc=food.get("zinc"),
        selenium=food.get("selenium"),
        microorganisms=food.get("microorganisms"),
        total_microorganisms=food.get("total_microorganisms")
        or food.get("total_lactic_acid_microorganisms"),
    )
    session.add(food)
    await session.commit()

    return JSONResponse(content=food.to_dict(), status_code=201)
