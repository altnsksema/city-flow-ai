import json

from aiokafka import AIOKafkaProducer

producer = None


async def start_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    await producer.start()


async def stop_producer():
    global producer
    if producer:
        await producer.stop()


async def send_station_update(station_id: int, current_load: float):
    global producer
    if not producer:
        return
    message = {
        "station_id": station_id,
        "current_load": current_load,
    }
    await producer.send_and_wait(
        "station.updates",
        json.dumps(message).encode("utf-8"),
    )
