from datetime import datetime
from app.models import Reminder
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


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
    query = select(Reminder).where(Reminder.id == reminder_id).where(Reminder.user_id == user.id)
    result = await session.execute(query)
    result = await result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/reminders")
async def get_reminders():
    query = select(Reminder)
    session = await get_session()
    reminders = await session.scalars(query)
    return JSONResponse(content=[reminder.to_dict() for reminder in reminders], status_code=200)


@router.get("/api/reminders/{user_id}")
async def get_user_reminders(user_id: int):
    session = await get_session()
    user = await get_current_user()
    if user.id == user_id or user.id == 1:
        query = select(Reminder).where(Reminder.user_id == user_id)
        reminders = await session.scalars(query)
        return JSONResponse(content=[reminder.to_dict() for reminder in reminders], status_code=200)
    else:
        return JSONResponse(content={"message": "Not authorized"}, status_code=404)
    

@router.post("/api/reminders")
async def create_reminder(reminder: dict):
    user = await get_current_user()
    session = await get_session()
    reminder = await _validate_reminder(reminder)

    # if reminder:
    start_str = reminder.get("start")
    if start_str:
        start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
    else:
        start = None

    end_str = reminder.get("end")
    if end_str:
        end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
    else:
        end = None

    reminder = Reminder(
        user_id = user.id,
        title=reminder.get("title"),
        start=start,
        end=end
    )
    session.add(reminder)
    await session.commit()

    return JSONResponse(content=reminder.to_dict(), status_code=201)


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