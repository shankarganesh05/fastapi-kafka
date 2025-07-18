import redis
import json

r = redis.Redis(host='redis',port=6379,db=0,decode_responses=True)

def get_cached_order(order_id:int):
    data = r.get(f"order:{order_id}")
    return json.loads(data) if data else None
def set_cached_order(order_id:int,order:dict):
    r.set(f"order:{order_id}",json.dumps(order),ex=60)
