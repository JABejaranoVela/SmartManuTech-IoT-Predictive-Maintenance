from __future__ import annotations

import json

from confluent_kafka import Consumer, KafkaError

from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from app.processor import process_reading
from app.storage import init_db


def main() -> None:
    init_db()
    consumer = Consumer(
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "group.id": "smartmanutech-maintenance",
            "auto.offset.reset": "latest",
        }
    )
    consumer.subscribe([KAFKA_TOPIC])
    print(f"Consuming IoT readings from Kafka topic '{KAFKA_TOPIC}'...")
    try:
        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() != KafkaError._PARTITION_EOF:
                    print(f"Kafka error: {message.error()}")
                continue

            reading = json.loads(message.value().decode("utf-8"))
            result = process_reading(reading)
            print(
                f"stored reading={result['reading_id']} machine={result['machine_id']} "
                f"risk={result['risk_score']} alerts={result['alerts_created']}"
            )
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
