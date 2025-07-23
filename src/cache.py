import redis
import json
import os
from dotenv import load_dotenv
load_dotenv()
host = os.getenv("REDIS_HOST")
r = redis.Redis(host=host, port=6379, db=0, decode_responses=True)

def get_cached_order(order_id:int):
    data = r.get(f"order:{order_id}")
    return json.loads(data) if data else None
def set_cached_order(order_id:int,order:dict):
    r.set(f"order:{order_id}",json.dumps(order),ex=60)
# def set_cached_user(user_email:str,password:str):
#     r.set(f"user:{user_email}",json.dumps({"password": password}),ex=60)
# def get_cached_user(user_email:str):
#     data = r.get(f"user:{user_email}")
#     return json.loads(data) if data else None
def send_user(user:dict):
    r.hset("users", user['Email'], user['password'])
def get_user(user_email:str):
    if r.hexists("users", user_email):
        data = r.hget("users", user_email)
        return data
    return None