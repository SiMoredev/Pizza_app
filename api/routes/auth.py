
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from api.deps import get_db
from db.models import Users
#from authx import AuthX, AuthXConfig

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

#config = AuthXConfig()
#config.JWT_SECRET_KEY = "srfgggsgv"
#security = AuthX(config=config)

@auth_router.post("/auth")
async def auth_user():

    return {"message": "Authentication endpoint is working!"}

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
    new_user = Users(email=email, password=password)  # адаптируйте под вашу модель
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User registered successfully!"}

@auth_router.get("/login")
async def login_user():
    return {"message": "Login endpoint is working!"}