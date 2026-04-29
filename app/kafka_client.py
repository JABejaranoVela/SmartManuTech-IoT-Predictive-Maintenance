from __future__ import annotations

import json
from typing import Any

from confluent_kafka import Producer

from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


def publish_reading(reading: dict[str, Any]) -> None:
    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    producer.produce(KAFKA_TOPIC, json.dumps(reading).encode("utf-8"))
    producer.flush()
