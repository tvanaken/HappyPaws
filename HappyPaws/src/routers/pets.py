from datetime import datetime
from decimal import Decimal
from app.models import Breed, Pet
from app.utils import get_current_user, get_session
from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from routers.breeds import _get_breed_name

router = APIRouter()


def _validate_pet(pet: dict):
    if pet.get("name") is None:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if pet.get("breed") is None:
        raise HTTPException(status_code=400, detail="Breed cannot be empty")
    return pet


async def _get_pet(pet_id: int):
    session = await get_session()
    user = await get_current_user()
    query = select(Pet).where(Pet.id == pet_id).where(Pet.user_id == user.id).order_by(Pet.id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/pets")
async def get_all_pets():
    user = await get_current_user()
    query = select(Pet).order_by(Pet.id)
    session = await get_session()
    pets = await session.scalars(query)
    return JSONResponse(content=[pet.to_dict() for pet in pets], status_code=200)


@router.get("/api/pets")
async def get_pets_for_user():
    user = await get_current_user()
    query = select(Pet).where(Pet.user_id == user.id).order_by(Pet.id)
    session = await get_session()
    pets = await session.scalars(query)
    return JSONResponse(content=[pet.to_dict() for pet in pets], status_code=200)


@router.get("/api/pets/{pet_id}")
async def get_pet(pet_id: int):
    pet = await _get_pet(pet_id)
    if pet:
        return pet.to_dict()
    else:
        return JSONResponse(content={"message": "Not found."}, status_code=404)
    

@router.post("/api/pets")
async def create_pet(pet: dict):
    user = await get_current_user()
    session = await get_session()
    pet = _validate_pet(pet)
    breed = await _get_breed_name(pet.get("breed"))

    birthday_str = pet.get("birthday")
    if birthday_str:
        birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
    else:
        birthday = None

    pet = Pet( 
        user_id = user.id,
        breed_id = breed.id,
        name=pet.get("name"),
        age=int(pet.get("age")),
        weight=Decimal(pet.get("weight")),
        birthday=birthday
    )
    session.add(pet)
    await session.commit()

    return JSONResponse(content=pet.to_dict(), status_code=201)


@router.delete("/api/pets/{pet_id}")
async def delete_pet(pet_id: int):
    user = await get_current_user()
    pet = await _get_pet(pet_id)
    session = await get_session()
    if pet:
        await session.delete(pet)
        await session.commit()
        return JSONResponse(content={"message": "pet deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Not found."}, status_code=404)
    

@router.patch("/api/pets/{pet_id}")
async def update_pet(pet_id: int, pet_updates: dict):
    session = await get_session()
    pet = await _get_pet(pet_id)
    breed = await _get_breed_name(pet_updates.get("breed"))

    if not pet:
        return JSONResponse(content={"message": "Not found."}, status_code=404)

    if pet_updates.get("name") is not None:
        pet.name = pet_updates.get("name")
    if pet_updates.get("breed") is not None:
        pet.breed = breed
    if pet_updates.get("age") is not None:
        pet.age = int(pet_updates.get("age"))
    if pet_updates.get("weight") is not None:
        pet.weight = pet_updates.get("weight")
    if pet_updates.get("birthday") is not None:
        birthday_str = pet_updates.get("birthday")
        if birthday_str:
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
        else:
            birthday = None
        pet.birthday = birthday
    await session.commit()

    return JSONResponse(content=pet.to_dict(), status_code=200)