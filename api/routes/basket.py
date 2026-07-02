from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from api.deps import get_db
from db.models import Basket
from schemas import schemas
from dotenv import load_dotenv

load_dotenv()

basket_router = APIRouter(prefix="/basket", tags=["basket user"])

@basket_router.post("/add_pizza_on_basket")
async def add_pizza_on_basket(order: schemas.AddBasket, db: AsyncSession = Depends(get_db)):
    
    add_basket = Basket(
        pizza_id = order.pizza_id,
        user_email = order.user_email,
        pizza_value = order.pizza_value
    )
    
    db.add(add_basket)
    await db.commit()
    await db.refresh(add_basket)
    
    return {"message": "Pizza added successfully!", "add_basket_id": add_basket.id}

@basket_router.get("/user_busket")
async def get_basket_user(user_email: str, db: AsyncSession = Depends(get_db)):
    query = select(Basket).where(Basket.user_email == user_email)
    result = await db.execute(query)
    pizzas = result.scalars().all()
    return pizzas