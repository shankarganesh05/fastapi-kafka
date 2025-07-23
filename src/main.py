from fastapi import FastAPI,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from src.model import Order,getOrder,User,UserResponse
from src.utilis import hash,verify
from src.kafka_producer import send_kafka
from src.kafka_consumer import consume_func
from sqlmodel import SQLModel,Session,select
from src.db import engine,get_session,Orders,Users
from src.cache import get_cached_order,set_cached_order,send_user,get_user
from src.outh import create_token
from prometheus_fastapi_instrumentator import Instrumentator
import threading

# async def lifespan(app: FastAPI):
#     SQLModel.metadata.create_all(engine)
#     t= threading.Thread(target=consume_order,daemon=True)
#     t.start()

app = FastAPI()
Instrumentator().instrument(app).expose(app)
#SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def startup_event():
    SQLModel.metadata.create_all(engine)
    def safe_consume(topic):
        try:
            print(f"Starting consumer for topic: {topic}")
            consume_func(topic)
        except Exception as e:
            print(f"Error in consumer for topic {topic}: {e}")
    t = threading.Thread(target=safe_consume, args=('orders',), daemon=True)
    # u = threading.Thread(target=safe_consume, args=('users',), daemon=True)
    t.start()
    # u.start()


@app.post("/orders/",status_code = status.HTTP_201_CREATED)
async def create_order(order: Order):
    order_data = order.dict()
    send_kafka('orders', order_data)
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

@app.post("/users/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_user(user: User):
    user_data = user.model_dump()
    user_data['password'] = hash(user.password)
    #send_kafka('users', user_data)
    if get_cache(user_data['Email']):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    send_user(user_data)
    return  user_data
@app.post("/login",status_code=status.HTTP_202_ACCEPTED,)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_session)):
    cache = get_user(user_credentials.username)
    print(f"password:{cache}")
    if cache and verify(user_credentials.password, cache):
        token_data = create_token(data={"Email":user_credentials.username})
        
        return {"access_token": token_data,"token_type":"Bearer"}
    # user = db.exec(select(Users).where(Users.Email == user_credentials.username)).first()
    # if not user or not verify(user_credentials.password, user.password):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # #set_cached_user(user.Email, user.password)
    # return {"access_token": create_token(data={"Email":user.Email}),"token_type":"Bearer"}