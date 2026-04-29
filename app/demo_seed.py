from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.analytics import calculate_risk_score, classify_status
from app.processor import process_reading


def build_reading(
    *,
    timestamp: datetime,
    machine_id: str,
    temperature_c: float,
    vibration_mm_s: float,
    production_speed_pct: float,
    energy_kw: float,
    error_code: str = "OK",
) -> dict[str, Any]:
    reading = {
        "timestamp": timestamp.isoformat(),
        "machine_id": machine_id,
        "temperature_c": temperature_c,
        "vibration_mm_s": vibration_mm_s,
        "production_speed_pct": production_speed_pct,
        "energy_kw": energy_kw,
        "error_code": error_code,
    }
    reading["risk_score"] = calculate_risk_score(reading)
    reading["status"] = classify_status(reading["risk_score"])
    return reading


def demo_readings() -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    cases = [
        {
            "machine_id": "SMT-01",
            "temperature_c": 66.2,
            "vibration_mm_s": 3.4,
            "production_speed_pct": 94.0,
            "energy_kw": 37.5,
            "error_code": "OK",
        },
        {
            "machine_id": "SMT-02",
            "temperature_c": 88.4,
            "vibration_mm_s": 4.2,
            "production_speed_pct": 86.0,
            "energy_kw": 41.3,
            "error_code": "OK",
        },
        {
            "machine_id": "SMT-03",
            "temperature_c": 70.0,
            "vibration_mm_s": 8.9,
            "production_speed_pct": 84.0,
            "energy_kw": 40.5,
            "error_code": "OK",
        },
        {
            "machine_id": "SMT-04",
            "temperature_c": 68.0,
            "vibration_mm_s": 4.0,
            "production_speed_pct": 61.5,
            "energy_kw": 39.0,
            "error_code": "OK",
        },
        {
            "machine_id": "SMT-02",
            "temperature_c": 73.0,
            "vibration_mm_s": 5.0,
            "production_speed_pct": 82.0,
            "energy_kw": 57.2,
            "error_code": "OK",
        },
        {
            "machine_id": "SMT-03",
            "temperature_c": 76.0,
            "vibration_mm_s": 5.4,
            "production_speed_pct": 80.0,
            "energy_kw": 44.0,
            "error_code": "E-204",
        },
        {
            "machine_id": "SMT-04",
            "temperature_c": 93.5,
            "vibration_mm_s": 10.8,
            "production_speed_pct": 58.0,
            "energy_kw": 61.0,
            "error_code": "E-309",
        },
    ]
    return [
        build_reading(timestamp=now + timedelta(seconds=index), **case)
        for index, case in enumerate(cases)
    ]


def seed_demo_data() -> dict[str, Any]:
    results = [process_reading(reading) for reading in demo_readings()]
    return {
        "readings_created": len(results),
        "alerts_created": sum(result["alerts_created"] for result in results),
        "alert_codes": sorted(
            {
                alert["code"]
                for result in results
                for alert in result["alerts"]
            }
        ),
    }


if __name__ == "__main__":
    print(seed_demo_data())
