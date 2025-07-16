from fastapi import FastAPI,Depends,status,HTTPException
from typing import List
from src.model import Order,getOrder
from src.kafka_producer import send_order_kafka
from src.kafka_consumer import consume_order
from sqlmodel import SQLModel,Session,select
from src.db import engine,get_session,Orders
from src.cache import get_cached_order,set_cached_order
import threading

# async def lifespan(app: FastAPI):
#     SQLModel.metadata.create_all(engine)
#     t= threading.Thread(target=consume_order,daemon=True)
#     t.start()

app = FastAPI()
#SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def startup_event():
    SQLModel.metadata.create_all(engine)
    t= threading.Thread(target=consume_order,daemon=True)
    t.start()


@app.post("/orders/",status_code = status.HTTP_201_CREATED)
async def create_order(order: Order):
    order_data = order.dict()
    send_order_kafka(order_data)
    return {"message": "Order Received", "order": order_data}

@app.get("/orders/",response_model=List[getOrder])
def get_order(db: Session= Depends(get_session)):
    orders = db.exec(select(Orders)).all()
    print(orders)
    return orders

@app.get("/orders/{order_id}",response_model=getOrder)
def get_order(order_id:int,db: Session= Depends(get_session)):
    cache = get_cached_order(order_id)
    if cache:
        return cache
    order = db.get(Orders,order_id)
    if order:
        
        set_cached_order(order_id,order.model_dump_json())
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} does not exist")

