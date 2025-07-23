from pydantic import BaseModel,EmailStr
from datetime import datetime

class Order(BaseModel):
    item: str
    quantity: int
    price_per_item: float
class User(BaseModel):
    Email: EmailStr
    password: str
class UserResponse(BaseModel):
    Email: EmailStr
class getOrder(Order):
    order_id: int
    created_at:datetime
class getUsers(User):
    Email: EmailStr
    id: int


