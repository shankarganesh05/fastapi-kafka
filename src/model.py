from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    item: str
    quantity: int
    price_per_item: float

