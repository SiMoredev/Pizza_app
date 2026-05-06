
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response
from api.deps import get_db
from db.models import Users
import bcrypt
from authx import AuthX, AuthXConfig
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

config = AuthXConfig(
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_ACCESS_COOKIE_NAME="access_token",
)

auth = AuthX(config=config)

@auth_router.post("/register")
async def register_user(email: str, password: str, db: AsyncSession = Depends(get_db)):

    if not email or not password:
        return {"error": "Username or password are required."}
    
    # Проверяем, существует ли пользователь (асинхронно)
    query = select(Users).where(Users.email == email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this name already exists!"
        )
    
    # Создаем нового пользователя
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    new_user = Users(
        email=email, 
        password=hashed_password.decode('utf-8')
        )  # адаптируйте под вашу модель
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User registered successfully!"}

@auth_router.post("/login")
async def login_user(response: Response, email: str, password: str, db: AsyncSession = Depends(get_db)):
    
    query = select(Users).where(Users.email == email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if not existing_user or not bcrypt.checkpw(password.encode("utf-8"), existing_user.password.encode("utf-8")):
        raise HTTPException(
            status_code=401,
            detail="Not valid email or password"
        )
    
    access_token = auth.create_access_token(uid=email)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,  # 30 минут в секундах
        samesite="lax",
        secure=False,  # True в продакшене с HTTPS
        path="/"
    )

    return {"message": "Login successful!", "access_token": access_token}