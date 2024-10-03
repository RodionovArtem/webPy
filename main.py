from fastapi import FastAPI
from handlers import users_handler
from schemas.user import UserCreate
from database import metadata, engine, database
from models import users
from models.Users import UserRole

metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()   

@app.get("/users/")
async def read_users():
       return await users_handler.read_users(database)

@app.post("/users/")
async def create_user(user: UserCreate, role: UserRole):
    return await users_handler.create_user(user,database)
