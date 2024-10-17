from fastapi import FastAPI, Depends
from handlers import users_handler
from schemas.user import UserCreate, UserAuthorize
from database import metadata, engine, database
from models import users
from models.Users import UserRole
from utils.token import validate_token_and_role

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

@app.put("/users/authorize/")
async def authorize_user(user: UserAuthorize):
    return await users_handler.authorize_user(user, database)

@app.get("/with-credentials")
async def check_credentials(user = Depends(validate_token_and_role([ "approved_user", "admin"]))):
    return {"msg": "Welcome allowed user"}

@app.get("/without-credentials")
async def check_credentials():
     return {"msg": "Welcome all"}