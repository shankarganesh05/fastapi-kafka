from fastapi import FastAPI,Depends
from typing import List
from src.model import Order,getOrder
from src.kafka_producer import send_order_kafka
from src.kafka_consumer import consume_order
from sqlmodel import SQLModel,Session,select
from src.db import engine,get_session,Orders
import threading

app = FastAPI()
SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def startup_event():
    t= threading.Thread(target=consume_order,daemon=True)
    t.start()


@app.post("/orders/")
async def create_order(order: Order):
    order_data = order.dict()
    send_order_kafka(order_data)
    return {"message": "Order Received", "order": order_data}

@app.get("/orders/",response_model=List[getOrder])
def get_order(db: Session= Depends(get_session)):
    orders = db.exec(select(Orders)).all()
    print(orders)
    return orders


