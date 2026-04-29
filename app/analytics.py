from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AlertRule:
    code: str
    severity: str
    message: str
    recommendation: str


def calculate_risk_score(reading: dict[str, Any]) -> int:
    temp_score = max(0, min(30, int((reading["temperature_c"] - 65) * 1.5)))
    vibration_score = max(0, min(25, int((reading["vibration_mm_s"] - 4) * 6)))
    speed_score = max(0, min(15, int((85 - reading["production_speed_pct"]) * 0.8)))
    energy_score = max(0, min(15, int((reading["energy_kw"] - 42) * 1.5)))
    error_score = 15 if reading["error_code"] != "OK" else 0
    return max(0, min(100, temp_score + vibration_score + speed_score + energy_score + error_score))


def classify_status(risk_score: int) -> str:
    if risk_score >= 70:
        return "critical"
    if risk_score >= 40:
        return "warning"
    return "healthy"


def detect_alerts(reading: dict[str, Any]) -> list[dict[str, str]]:
    alerts: list[AlertRule] = []

    if reading["temperature_c"] >= 82:
        alerts.append(
            AlertRule(
                "TEMP_HIGH",
                "critical",
                "Temperatura alta en la maquina.",
                "Revisar ventilacion, lubricacion y carga de trabajo.",
            )
        )

    if reading["vibration_mm_s"] >= 7.0:
        alerts.append(
            AlertRule(
                "VIBRATION_HIGH",
                "critical",
                "Vibracion excesiva detectada.",
                "Inspeccionar rodamientos, alineacion y desgaste mecanico.",
            )
        )

    if reading["production_speed_pct"] <= 72:
        alerts.append(
            AlertRule(
                "SPEED_LOW",
                "warning",
                "Caida de velocidad de produccion.",
                "Comprobar cuellos de botella y alimentacion de materiales.",
            )
        )

    if reading["energy_kw"] >= 52:
        alerts.append(
            AlertRule(
                "ENERGY_HIGH",
                "warning",
                "Consumo energetico anomalo.",
                "Analizar eficiencia del motor y posibles rozamientos.",
            )
        )

    if reading["error_code"] != "OK":
        alerts.append(
            AlertRule(
                "ERROR_EVENT",
                "critical",
                f"Evento de error reportado: {reading['error_code']}.",
                "Revisar historico de fallos y planificar mantenimiento.",
            )
        )

    risk_score = int(reading["risk_score"])
    if risk_score >= 70:
        alerts.append(
            AlertRule(
                "PREDICTIVE_RISK_HIGH",
                "critical",
                "Riesgo predictivo alto por combinacion de variables.",
                "Programar parada controlada antes de fallo no planificado.",
            )
        )

    return [alert.__dict__ for alert in alerts]
