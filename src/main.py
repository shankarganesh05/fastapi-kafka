from fastapi import FastAPI
from src.model import Order
from src.kafka-producer import send_order_kafka

app = FastAPI()

@app.post("/orders/")
async def create_order(order: Order):
    order_data = order.dict()
    send_order_kafka(order_data)
    return {"message": "Order Received", "order": order_data}

