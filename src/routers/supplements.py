from app.models import Supplement
from app.utils import get_session
from sqlalchemy import select

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/supplements")
async def get_supplements():
    query = select(Supplement)
    session = await get_session()
    supplements = await session.scalars(query)
    return JSONResponse(content=[supplement.to_dict() for supplement in supplements], status_code=200)


@router.post("/api/supplement")
async def create_supplement(supplement: dict):
    session = await get_session()

    supplement = Supplement(
        name = supplement.get("name"),
        description = supplement.get("description"),
        ailment = supplement.get("Health Condition")
    )
    session.add(supplement)
    await session.commit()

    return JSONResponse(content=supplement.to_dict(), status_code=201)