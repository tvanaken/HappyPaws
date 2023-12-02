from app.models import Reminder
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/reminders")
async def get_reminders():
    query = select(Reminder)
    session = await get_session()
    reminders = await session.scalars(query)
    return JSONResponse(content=[reminder.to_dict() for reminder in reminders], status_code=200)