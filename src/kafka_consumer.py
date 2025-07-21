from kafka import KafkaConsumer
from src.db import get_session,Orders,Users
from src.model import Order
import json

def consume_func(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset = 'earliest',
        group_id=f'{topic}-processor-group',
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    if topic == 'orders':
        with get_session() as session:
            for message in consumer:
                order_data = message.value
                order = Orders(**order_data)
                print(order)

                session.add(order)
                session.commit()
    elif topic == 'users':
        with get_session() as session:
            for message in consumer:
                user_data = message.value
                user = Users(**user_data)
                print(user)

                session.add(user)
                session.commit()
