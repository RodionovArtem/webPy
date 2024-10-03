from fastapi import HTTPException
from sqlalchemy import select, insert
from utils.password import hash_password, verify_password
from models import users
from databases import Database
from schemas.user import UserCreate
from models.Users import UserRole, users

async def create_user(user: UserCreate, db: Database, role: UserRole = "user"):
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
