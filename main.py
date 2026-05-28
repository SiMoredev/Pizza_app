from fastapi import FastAPI
from dotenv import load_dotenv
from db.database import Base, engine
from api.routes.auth import auth_router
from api.routes.pizzas import pizzas_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_login_shield import LoginShieldMiddleware

load_dotenv()

create_all = Base.metadata.create_all

app = FastAPI()
app.include_router(auth_router)
app.include_router(pizzas_router)
app.add_middleware(LoginShieldMiddleware, login_path="/auth/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)