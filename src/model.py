from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):
    item: str
    quantity: int
    price_per_item: float
class getOrder(Order):
    order_id: int
