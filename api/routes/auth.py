
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from api.deps import get_db
from db.models import Users
from authx import AuthX, AuthXConfig

router = APIRouter(prefix="/auth", tags=["Authentication"])

config = AuthXConfig()
config.JWT_SECRET_KEY = "srfgggsgv"

security = AuthX(config=config)

@router.post("/auth")
async def auth_user():

    return {"message": "Authentication endpoint is working!"}

@router.post("/register")
async def register_user(username: str, password: str, db: AsyncSession = Depends(get_db)):
    if not username or not password:
        return {"error": "Username or password are required."}
    
    # Проверяем, существует ли пользователь (асинхронно)
    query = select(Users).where(Users.username == username)  # замените username на ваше поле
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        return {"error": "User with this name already exists!"}
    
    # Создаем нового пользователя
    new_user = Users(username=username, password=password)  # адаптируйте под вашу модель
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User registered successfully!"}

@router.get("/login")
async def login_user():
    return {"message": "Login endpoint is working!"}