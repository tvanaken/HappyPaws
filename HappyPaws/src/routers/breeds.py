from app.models import Breed
from app.utils import get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

router = APIRouter()


async def _validate_breed(breed: dict):
    if breed.get("name") is None:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    return breed


async def _get_breed(breed_id: int):
    session = await get_session()
    query = select(Breed).where(Breed.id == breed_id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


async def _get_breed_name(breed_id: int):
    session = await get_session()
    query = select(Breed).where(Breed.id == breed_id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0].name
    else:
        return None


@router.get("/api/breeds")
async def get_breeds(search: str = Query(None, min_length=2)):
    session = await get_session()
    query = select(Breed)
    if search:
        query = query.where(Breed.name.ilike(f"%{search}%"))
    breeds = await session.scalars(query)
    return JSONResponse(content=[breed.to_dict() for breed in breeds], status_code=200)


# @router.get("/api/breeds/{name}")
# async def get_breed(name: str):
#     breed = await _get_breed_name(name)
#     if breed:
#         return breed.to_dict()
#     else:
#         return JSONResponse(content={"message": "Not found."}, status_code=404)


@router.get("/api/breeds/{breed_id}")
async def get_breed(breed_id: int):
    breed = await _get_breed(breed_id)
    if breed:
        return breed.to_dict()
    else:
        return JSONResponse(content={"message": "Not found."}, status_code=404)


@router.post("/api/breeds")
async def create_breed(breed: dict):
    session = await get_session()
    breed = await _validate_breed(breed)

    breed = Breed(
        name=breed.get("name"),
        weights=breed.get("weights"),
        breed_description=breed.get("breed_description"),
        health_description=breed.get("health_description"),
        groom_description=breed.get("groom_description"),
        nutrition_description=breed.get("nutrition_description"),
        max_weight=breed.get("max_weight"),
        size=breed.get("size"),
    )
    session.add(breed)
    await session.commit()

    return JSONResponse(content=breed.to_dict(), status_code=201)


# @router.delete("/api/breeds/{name}")
# async def delete_breed(name: str):
#     session = await get_session()
#     breed = await _get_breed_name(name)
#     if breed:
#         await session.delete(breed)
#         await session.commit()
#         return JSONResponse(content={"message": "breed deleted"}, status_code=200)
#     else:
#         return JSONResponse(content={"message": "Not found."}, status_code=404)


@router.patch("/api/breeds/{breed_id}")
async def update_breed(breed_id: int, breed_updates: dict):
    session = await get_session()
    breed = await _get_breed(breed_id)
    if not breed:
        return JSONResponse(content={"message": "Not found."}, status_code=404)

    # modify values based on request body:
    if breed_updates.get("name") is not None:
        breed.name = breed_updates.get("name")
    await session.commit()

    return JSONResponse(content=breed.to_dict(), status_code=200)
