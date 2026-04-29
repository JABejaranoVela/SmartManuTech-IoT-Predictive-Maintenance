from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Any

from app.analytics import calculate_risk_score, classify_status
from app.config import MACHINE_IDS


def generate_reading(machine_id: str | None = None) -> dict[str, Any]:
    machine_id = machine_id or random.choice(MACHINE_IDS)
    anomaly_mode = random.random() < 0.22

    temperature = random.uniform(58, 76)
    vibration = random.uniform(2.0, 5.2)
    speed = random.uniform(82, 99)
    energy = random.uniform(31, 45)
    error_code = "OK"

    if anomaly_mode:
        anomaly_type = random.choice(["temp", "vibration", "speed", "energy", "error", "combined"])
        if anomaly_type in ["temp", "combined"]:
            temperature = random.uniform(82, 96)
        if anomaly_type in ["vibration", "combined"]:
            vibration = random.uniform(7.0, 11.5)
        if anomaly_type in ["speed", "combined"]:
            speed = random.uniform(52, 72)
        if anomaly_type in ["energy", "combined"]:
            energy = random.uniform(52, 64)
        if anomaly_type in ["error", "combined"]:
            error_code = random.choice(["E-101", "E-204", "E-309"])

    reading = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "machine_id": machine_id,
        "temperature_c": round(temperature, 2),
        "vibration_mm_s": round(vibration, 2),
        "production_speed_pct": round(speed, 2),
        "energy_kw": round(energy, 2),
        "error_code": error_code,
    }
    reading["risk_score"] = calculate_risk_score(reading)
    reading["status"] = classify_status(reading["risk_score"])
    return reading
