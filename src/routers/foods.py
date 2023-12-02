from app.models import Food
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
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
        type = food.get("type"),
        name = food.get("name"),
        ingredients = food.get("ingredients"),
        crude_protein = food.get("crude_protein"),
        crude_fat = food.get("crude_fat"),
        crude_fiber = food.get("crude_fiber"),
        moisture = food.get("moisture"),
        dietary_starch = food.get("dietary_starch"),
        epa = food.get("epa"),
        calcium = food.get("calcium"),
        phosphorus = food.get("phosphorus"),
        vitamin_e = food.get("vitamin_e"),
        omega_6 = food.get("omega_6"),
        omega_3 = food.get("omega_3"),
        glucosamine = food.get("glucosamine"),
        microorganisms = food.get("microorganisms")
    )
    session.add(food)
    await session.commit()

    return JSONResponse(content=food.to_dict(), status_code=201)