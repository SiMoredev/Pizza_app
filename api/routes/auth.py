
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from api.deps import get_db
from db.models import Users
import bcrypt
#from authx import AuthX, AuthXConfig

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

#config = AuthXConfig()

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

@auth_router.get("/login")
async def login_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    
    query = select(Users).where(Users.email == email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if not existing_user or not bcrypt.checkpw(password.encode("utf-8"), existing_user.password.encode("utf-8")):
        raise HTTPException(
            status_code=401,
            detail="Not valid email or password"
        )
    
    #config.JWT_SECRET_KEY = "srfgggsgv"
    #security = AuthX(config=config)
    
    return {"message": "Login successful!"}