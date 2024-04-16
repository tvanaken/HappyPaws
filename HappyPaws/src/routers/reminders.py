from datetime import datetime
from typing import Optional

from app.models import Reminder, User
from app.models.login import get_current_user
from app.routers.users import oauth2_scheme
from app.utils import get_session
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


class ReminderCreate(BaseModel):
    title: str
    start: datetime
    end: Optional[datetime] = None
    recurrence: Optional[str] = None


async def _validate_reminder(reminder: dict):
    if reminder.get("title") is None:
        raise HTTPException(status_code=400, detail="Must define a title")
    if reminder.get("start") is None:
        raise HTTPException(status_code=400, detail="Must give a start date")
    if reminder.get("end") is None:
        raise HTTPException(status_code=400, detail="Must state a end date")
    return reminder


async def _get_reminder(reminder_id: int):
    session = await get_session()
    user = await get_current_user()
    query = (
        select(Reminder)
        .where(Reminder.id == reminder_id)
        .where(Reminder.user_id == user.id)
    )
    result = await session.execute(query)
    result = await result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/reminders")
async def get_reminders(user: User = Depends(get_current_user)):
    session = await get_session()
    query = select(Reminder).where(Reminder.user_id == user.id)
    reminders = await session.scalars(query)
    return JSONResponse(
        content=[reminder.to_dict() for reminder in reminders], status_code=200
    )


@router.get("/api/reminders/{user_id}")
async def get_user_reminders(user_id: int):
    session = await get_session()
    user = await get_current_user()
    if user.id == user_id or user.id == 1:
        query = select(Reminder).where(Reminder.user_id == user_id)
        reminders = await session.scalars(query)
        return JSONResponse(
            content=[reminder.to_dict() for reminder in reminders], status_code=200
        )
    else:
        return JSONResponse(content={"message": "Not authorized"}, status_code=404)


@router.post("/api/reminders", response_model=ReminderCreate)
async def create_reminder(
    reminder_data: ReminderCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    user = await get_current_user(token, session)

    reminder = Reminder(
        user_id=user.id,
        title=reminder_data.title,
        start=reminder_data.start,
        end=reminder_data.end,
    )
    session.add(reminder)
    await session.commit()
    await session.refresh(reminder)

    return JSONResponse(content={"message": "Reminder created"}, status_code=201)


@router.delete("/api/reminders/{reminder_id}")
async def delete_reminder(reminder_id: int):
    user = await get_current_user()
    session = await get_session()
    reminder = await _get_reminder(reminder_id)
    if reminder:
        await session.delete(reminder)
        await session.commit()
        return JSONResponse(content={"message": "Reminder deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Reminder not found"}, status_code=404)


@router.patch("/api/reminders/{reminder_id}")
async def update_reminder(reminder_id: int, reminder_updates: dict):
    session = await get_session()
    reminder = await _get_reminder(reminder_id)

    if not reminder:
        return JSONResponse(content={"message": "Reminder not found"}, status_code=404)

    if reminder_updates.get("title") is not None:
        reminder.title = reminder_updates.get("title")
    if reminder_updates.get("start") is not None:
        start_str = reminder_updates.get("start")
        if start_str:
            start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
        else:
            start = None
        reminder.start = start
    if reminder_updates.get("end") is not None:
        end_str = reminder_updates.get("end")
        if end_str:
            end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
        else:
            end = None
        reminder.end = end

    await session.commit()

    return JSONResponse(content=reminder.to_dict(), status_code=200)
