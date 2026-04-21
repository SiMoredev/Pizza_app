from fastapi import FastAPI
from dotenv import load_dotenv
from database import Base

load_dotenv()

#db

app = FastAPI()

@app.get("/get_pizzas")
async def get_pizzas():
    return {"message": "Pizza API is alive!"}

@app.post("/auth")
async def auth_user():
    pass