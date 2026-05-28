from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response
from api.deps import get_db
from db.models import PizzasCatalog
from schemas import schemas
import os
from dotenv import load_dotenv

load_dotenv()

pizzas_router = APIRouter(prefix="/pizzas", tags=["CRUD pizzas"])

@pizzas_router.post("/add_pizza")
async def add_pizza(pizza: schemas.AddPizzas, db: AsyncSession = Depends(get_db)):
    
    new_pizza = PizzasCatalog(
        namePizza = pizza.namePizza,
        cost = pizza.cost,
        ingredients = pizza.ingredients,
        picturePizza = pizza.picturePizza,
        size = pizza.size,
        thicknessDough = pizza.thicknessDough
    )
    
    db.add(new_pizza)
    await db.commit()
    await db.refresh(new_pizza)
    
    return {"message": "Pizza added successfully!", "pizza_id": new_pizza.id}