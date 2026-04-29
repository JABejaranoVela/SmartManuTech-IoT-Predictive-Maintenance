from __future__ import annotations

import time

from app.config import KAFKA_TOPIC
from app.kafka_client import publish_reading
from app.simulator import generate_reading


def main() -> None:
    print(f"Sending IoT readings to Kafka topic '{KAFKA_TOPIC}'...")
    while True:
        reading = generate_reading()
        publish_reading(reading)
        print(
            f"{reading['timestamp']} {reading['machine_id']} "
            f"risk={reading['risk_score']} status={reading['status']}"
        )
        time.sleep(1)


if __name__ == "__main__":
    main()
