from kafka import KafkaConsumer
from src.db import get_session,Orders
from src.model import Order
import json

def consume_order():
    consumer = KafkaConsumer(
        'orders',
        bootstrap_servers='kafka:9092',
        auto_offset_reset = 'earliest',
        group_id='order-processor-group',
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    with get_session() as session:
        for message in consumer:
            order_data = message.value
            order = Orders(**order_data)
            print(order)

            session.add(order)
            session.commit()