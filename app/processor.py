from __future__ import annotations

from typing import Any

from app.analytics import detect_alerts
from app.storage import save_reading


def process_reading(reading: dict[str, Any]) -> dict[str, Any]:
    alerts = detect_alerts(reading)
    reading_id = save_reading(reading, alerts)
    return {
        "reading_id": reading_id,
        "machine_id": reading["machine_id"],
        "status": reading["status"],
        "risk_score": reading["risk_score"],
        "alerts_created": len(alerts),
        "alerts": alerts,
    }
