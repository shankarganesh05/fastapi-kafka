from pydantic import BaseModel,EmailStr
from datetime import datetime

class Order(BaseModel):
    item: str
    quantity: int
    price_per_item: float
class Users(BaseModel):
    email: EmailStr
    password: str
class getOrder(Order):
    order_id: int
    created_at:datetime
class getUsers(Users):
    email: EmailStr
    id: int


