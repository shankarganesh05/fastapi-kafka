from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_order_kafka(order_data:dict):
    producer.send('orders', order_data)
    producer.flush()

