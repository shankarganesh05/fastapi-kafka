from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    item: str
    quantity: int
    price_per_item: float
class getOrder(Order):
    order_id: int
    created_at:datetime
