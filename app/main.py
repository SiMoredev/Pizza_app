from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/get_pizzas")
async def get_pizzas():
    return {"message": "Pizza API is alive!"}
