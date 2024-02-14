from contextlib import asynccontextmanager

from app.routers import users, breeds, foods, reminders, pets, supplements
from app.utils import get_session

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # creates DB session session when the application starts
    print("lifespan start...")
    session = await get_session()

    yield

    # closes session when the application stops
    print("lifespan end...")
    await session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(breeds.router)
app.include_router(reminders.router)
app.include_router(foods.router)
app.include_router(pets.router)
app.include_router(supplements.router)


app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
