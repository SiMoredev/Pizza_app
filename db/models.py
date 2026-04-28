from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class PizzasCatalog(Base):

    __tablename__ = "PizzasCatalog"

    id = Column(Integer, primary_key=True, index=True)

    namePizza = Column(String(100), index=True, nullable=False)
    cost = Column(Integer, nullable=False)
    ingridients = Column(String, nullable=False)
    picturePizza = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    thicknessDough = Column(Boolean, nullable=False)

class Users(Base):

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)