from pydantic import BaseModel

class AddPizzas(BaseModel):
    
    namePizza: str
    cost: int
    ingredients: str
    picturePizza: str
    size: int
    thicknessDough: bool

    class Config:
        from_attributes = True

class AddBasket(BaseModel):

    pizza_id: int
    user_email: str
    pizza_value: int

    class Config:
        from_attributes = True