from datetime import datetime
from decimal import Decimal

from app.models import Breed, Pet
from app.models.login import get_current_user
from app.routers.users import oauth2_scheme
from app.utils import get_session
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from routers.breeds import _get_breed_name
import boto3
from botocore.exceptions import ClientError

router = APIRouter()


class PetCreate(BaseModel):
    name: str
    breed1: str
    breed2: str | None = None
    weight: Decimal
    birthday: datetime | None = None
    age: int | None = None
    bio: str | None = None
    image_url: str | None = None
    activity_level: str


def _validate_pet(pet: dict):
    """
    Validates a pet dictionary.

    Args:
        pet (dict): The pet dictionary to be validated.

    Raises:
        HTTPException: If the name or breed is missing in the pet dictionary.

    Returns:
        dict: The validated pet dictionary.
    """
    if pet.get("name") is None:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if pet.get("breed") is None:
        raise HTTPException(status_code=400, detail="Breed cannot be empty")
    return pet


async def get_breed_id_by_name(session, breed_name):
    """
    Retrieves the breed ID based on the given breed name.

    Parameters:
    - session: The database session to use for the query.
    - breed_name: The name of the breed to search for.

    Returns:
    - The breed ID if found, otherwise None.
    """
    breed_id = await session.execute(select(Breed.id).where(Breed.name == breed_name))
    return breed_id.scalar_one_or_none()


async def _get_pet(
    pet_id: int,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieves a pet with the specified pet_id that belongs to the authenticated user.

    Parameters:
        pet_id (int): The ID of the pet to retrieve.
        token (str, optional): The authentication token. Defaults to Depends(oauth2_scheme).
        session (AsyncSession, optional): The database session. Defaults to Depends(get_session).

    Returns:
        Pet: The pet object if found, None otherwise.
    """
    user = await get_current_user(token, session)
    query = (
        select(Pet)
        .where(Pet.id == pet_id)
        .where(Pet.user_id == user.id)
        .order_by(Pet.id)
    )
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/pets")
async def get_pets_for_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
):
    """
    Retrieves the pets associated with the authenticated user.

    Parameters:
        token (str): The authentication token.
        session (AsyncSession): The asynchronous database session.

    Returns:
        JSONResponse: The JSON response containing the pets for the user.
    """
    user = await get_current_user(token, session)
    query = select(Pet).where(Pet.user_id == user.id).order_by(Pet.id)
    session = await get_session()
    pets = await session.scalars(query)
    return JSONResponse(content=[pet.to_dict() for pet in pets], status_code=200)


@router.get("/api/pets/{pet_id}")
async def get_pet(
    pet_id: int,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieves information about a pet.

    Args:
        pet_id (int): The ID of the pet to retrieve.
        token (str, optional): The authentication token. Defaults to Depends(oauth2_scheme).
        session (AsyncSession, optional): The database session. Defaults to Depends(get_session).

    Returns:
        dict: A dictionary containing the pet information if found, otherwise a JSONResponse with a "Not found" message and a 404 status code.
    """
    pet = await _get_pet(pet_id, token, session)
    if pet:
        return pet.to_dict()
    else:
        return JSONResponse(content={"message": "Not found."}, status_code=404)


@router.post("/api/pets", response_model=PetCreate)
async def create_pet(
    pet_data: PetCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new pet.

    Args:
        pet_data (PetCreate): The data for the new pet.
        token (str, optional): The authentication token. Defaults to Depends(oauth2_scheme).
        session (AsyncSession, optional): The database session. Defaults to Depends(get_session).

    Returns:
        JSONResponse: The response containing the created pet data.
    """
    user = await get_current_user(token, session)

    pet = Pet(
        user_id=user.id,
        breed_id1=await get_breed_id_by_name(session, pet_data.breed1),
        breed_id2=await get_breed_id_by_name(session, pet_data.breed2),
        name=pet_data.name,
        weight=pet_data.weight,
        birthday=pet_data.birthday,
        age=pet_data.age,
        bio=pet_data.bio,
        image_url=pet_data.image_url,
        activity_level=pet_data.activity_level,
    )
    session.add(pet)
    await session.commit()

    return JSONResponse(content=pet.to_dict(), status_code=201)


@router.delete("/api/pets/{pet_id}")
async def delete_pet(pet_id: int):
    """
    Delete a pet with the given pet_id.

    Parameters:
    - pet_id (int): The ID of the pet to be deleted.

    Returns:
    - JSONResponse: A JSON response indicating the status of the deletion.
    """
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
    """
    Update the information of a pet.
    Args:
        pet_id (int): The ID of the pet to be updated.
        pet_updates (dict): A dictionary containing the updated information of the pet.
    Returns:
        JSONResponse: The updated pet information in JSON format.
    Raises:
        JSONResponse: If the pet is not found, returns a JSON response with a "Not found" message and a status code of 404.
    """

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


@router.get("/api/s3PresignedUrl")
async def get_presigned_url(file_name: str):
    """
    Generates a presigned URL for uploading an image file to an S3 bucket.
    Args:
        file_name (str): The name of the file to be uploaded.
    Returns:
        dict: A dictionary containing the presigned URL.
    Raises:
        HTTPException: If there is an error generating the presigned URL.
    """
    print("Received file name: " + file_name)
    s3_client = boto3.client('s3')
    bucket_name = "happypawsproject"

    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': file_name, 'ContentType': 'image/jpeg'},
            ExpiresIn=3600)
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"url": presigned_url}