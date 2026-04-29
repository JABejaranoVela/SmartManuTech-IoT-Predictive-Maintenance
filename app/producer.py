from __future__ import annotations

import json
import time

from confluent_kafka import Producer

from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from app.simulator import generate_reading


def main() -> None:
    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    print(f"Sending IoT readings to Kafka topic '{KAFKA_TOPIC}'...")
    while True:
        reading = generate_reading()
        producer.produce(KAFKA_TOPIC, json.dumps(reading).encode("utf-8"))
        producer.flush()
        print(
            f"{reading['timestamp']} {reading['machine_id']} "
            f"risk={reading['risk_score']} status={reading['status']}"
        )
        time.sleep(1)


if __name__ == "__main__":
    main()
