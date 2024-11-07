from fastapi import HTTPException
from sqlalchemy import select, insert
from utils.password import hash_password, verify_password
from models import users
from databases import Database
from schemas.user import UserCreate, UserAuthorize
from models.Users import UserRole, users
from utils.token import create_access_token

async def create_user(user: UserCreate, db: Database, role: UserRole):
    query = users.select().where(users.c.email == user.email)
    existing_user = await db.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    pwd_hash = hashed_password.decode('utf-8')


    query = insert(users).values(
        name=user.name,
        email=user.email,
        hashed_password=pwd_hash,
        role=role)
    await db.execute(query)
    return {"name": user.name, "email": user.email, "role": role}

async def authorize_user(user: UserAuthorize, db: Database):
    query = users.select().where(users.c.email == user.email)
    existing_user = await db.fetch_one(query)
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if (verify_password(user.password,existing_user.hashed_password)):
        token = create_access_token(data={"sub": existing_user.name,"role":existing_user.role.value, "id":existing_user["id"]})
        return {"token":token}
        
    raise HTTPException(status_code=401, detail="User or password not correct")