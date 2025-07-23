from kafka import KafkaProducer
import json
import os
from dotenv import load_dotenv
load_dotenv()
host = os.getenv("KAFKA_HOST")
producer = KafkaProducer(
    bootstrap_servers=f'{host}:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_kafka(topic:str, data:dict):
    producer.send(topic, data)
    producer.flush()


