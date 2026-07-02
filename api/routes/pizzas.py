from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from api.deps import get_db
from db.models import PizzasCatalog
from schemas import schemas
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

@pizzas_router.get("")
async def get_all_pizzas(db: AsyncSession = Depends(get_db)):
    query = select(PizzasCatalog)
    result = await db.execute(query)
    pizzas = result.scalars().all()
    return pizzas

@pizzas_router.put("/update/{pizza_id}")
async def update_pizza(
    pizza_id: int,
    pizza_data: schemas.AddPizzas,
    db: AsyncSession = Depends(get_db)
):
    query = select(PizzasCatalog).where(PizzasCatalog.id == pizza_id)
    result = await db.execute(query)
    pizza = result.scalar_one_or_none()
    
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    
    # Обновляем поля
    pizza.namePizza = pizza_data.namePizza #type: ignore
    pizza.cost = pizza_data.cost #type: ignore
    pizza.ingredients = pizza_data.ingredients #type: ignore
    pizza.picturePizza = pizza_data.picturePizza #type: ignore
    pizza.size = pizza_data.size #type: ignore
    pizza.thicknessDough = pizza_data.thicknessDough #type: ignore
    
    await db.commit()
    await db.refresh(pizza)
    
    return {"message": "Pizza updated!", "pizza": pizza}

@pizzas_router.delete("/delete/{pizza_id}")
async def delete_pizza(
    pizza_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = select(PizzasCatalog).where(PizzasCatalog.id == pizza_id)
    result = await db.execute(query)
    pizza = result.scalar_one_or_none()
    
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    
    await db.delete(pizza)
    await db.commit()
    
    return {"message": "Pizza deleted!"}