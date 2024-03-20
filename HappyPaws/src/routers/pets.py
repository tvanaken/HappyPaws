from datetime import datetime
from decimal import Decimal
from app.models import Breed, Pet
from app.models.login import get_current_user
from app.routers.users import oauth2_scheme
from app.utils import get_session
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from routers.breeds import _get_breed_name
from pydantic import BaseModel


router = APIRouter()

class PetCreate(BaseModel):
    name: str
    breed1: str
    breed2: str | None = None
    weight: Decimal
    birthday: datetime | None = None


def _validate_pet(pet: dict):
    if pet.get("name") is None:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if pet.get("breed") is None:
        raise HTTPException(status_code=400, detail="Breed cannot be empty")
    return pet


async def get_breed_id_by_name(session, breed_name):
    breed_id = await session.execute(
        select(Breed.id).where(Breed.name == breed_name)
    )
    return breed_id.scalar_one_or_none()


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
async def get_pets_for_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    user = await get_current_user(token, session)
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
    

@router.post("/api/pets", response_model=PetCreate)
async def create_pet(pet_data: PetCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    user = await get_current_user(token, session)

    pet = Pet( 
        user_id = user.id,
        breed_id1 = await get_breed_id_by_name(session, pet_data.breed1),
        breed_id2 = await get_breed_id_by_name(session, pet_data.breed2),
        name = pet_data.name,
        weight = pet_data.weight,
        birthday = pet_data.birthday
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