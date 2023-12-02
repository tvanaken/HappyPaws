from app.models import Task
from app.utils import get_current_user, get_session
from sqlalchemy import select

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


def _validate_task(task: dict):
    if task.get("name") is None:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if task.get("description") is None:
        raise HTTPException(status_code=400, detail="Description cannot be empty")
    return task


async def _get_task(task_id: int):
    session = await get_session()
    user = await get_current_user()
    query = select(Task).where(Task.id == task_id).where(Task.user_id == user.id)
    result = await session.execute(query)
    result = result.fetchone()
    if result:
        return result[0]
    else:
        return None


@router.get("/api/tasks")
async def get_tasks():
    user = await get_current_user()
    query = select(Task).where(Task.user_id == user.id).order_by(Task.id)
    session = await get_session()
    tasks = await session.scalars(query)
    return JSONResponse(content=[task.to_dict() for task in tasks], status_code=200)


@router.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    task = await _get_task(task_id)
    if task:
        return task.to_dict()
    else:
        return JSONResponse(content={"message": "Not found."}, status_code=404)


@router.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    session = await get_session()
    task = await _get_task(task_id)
    if task:
        await session.delete(task)
        await session.commit()
        return JSONResponse(content={"message": "task deleted"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Not found."}, status_code=404)


@router.post("/api/tasks")
async def create_task(task: dict):
    user = await get_current_user()
    session = await get_session()
    task = _validate_task(task)

    task = Task(
        name=task.get("name"),
        description=task.get("description"),
        done=False,
        user_id=user.id,
    )
    session.add(task)
    await session.commit()

    return JSONResponse(content=task.to_dict(), status_code=201)


@router.patch("/api/tasks/{task_id}")
async def update_task(task_id: int, task_updates: dict):
    session = await get_session()
    task = await _get_task(task_id)
    if not task:
        return JSONResponse(content={"message": "Not found."}, status_code=404)

    # modify values based on request body:
    if task_updates.get("name") is not None:
        task.name = task_updates.get("name")
    if task_updates.get("description") is not None:
        task.description = task_updates.get("description")
    if task_updates.get("done") is not None:
        task.done = task_updates.get("done")
    await session.commit()

    return JSONResponse(content=task.to_dict(), status_code=200)
