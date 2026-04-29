from fastapi import FastAPI
from dotenv import load_dotenv
from db.database import Base, engine
from api.routes.auth import auth_router

load_dotenv()

create_all = Base.metadata.create_all

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Pizza App!"}