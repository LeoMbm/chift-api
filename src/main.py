import uvicorn
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from core.db import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from api.models import UserSchema, ResponseModel
from core.settings import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.post("/register")
async def register(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "Student added successfully.")
