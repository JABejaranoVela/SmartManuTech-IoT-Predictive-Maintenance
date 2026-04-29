from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any, Iterator

from app.config import DATA_DIR, DB_PATH


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                machine_id TEXT NOT NULL,
                temperature_c REAL NOT NULL,
                vibration_mm_s REAL NOT NULL,
                production_speed_pct REAL NOT NULL,
                energy_kw REAL NOT NULL,
                error_code TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                machine_id TEXT NOT NULL,
                code TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                reading_id INTEGER NOT NULL,
                FOREIGN KEY(reading_id) REFERENCES readings(id)
            )
            """
        )


def save_reading(reading: dict[str, Any], alerts: list[dict[str, str]]) -> int:
    init_db()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO readings (
                timestamp, machine_id, temperature_c, vibration_mm_s,
                production_speed_pct, energy_kw, error_code, risk_score, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reading["timestamp"],
                reading["machine_id"],
                reading["temperature_c"],
                reading["vibration_mm_s"],
                reading["production_speed_pct"],
                reading["energy_kw"],
                reading["error_code"],
                reading["risk_score"],
                reading["status"],
            ),
        )
        reading_id = int(cursor.lastrowid)
        for alert in alerts:
            conn.execute(
                """
                INSERT INTO alerts (
                    timestamp, machine_id, code, severity, message,
                    recommendation, reading_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    reading["timestamp"],
                    reading["machine_id"],
                    alert["code"],
                    alert["severity"],
                    alert["message"],
                    alert["recommendation"],
                    reading_id,
                ),
            )
        return reading_id


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def get_recent_readings(limit: int = 100) -> list[dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return rows_to_dicts(rows)


def get_recent_alerts(limit: int = 100) -> list[dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM alerts ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return rows_to_dicts(rows)


def get_machine_status() -> list[dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            WITH latest AS (
                SELECT r.*
                FROM readings r
                JOIN (
                    SELECT machine_id, MAX(id) AS max_id
                    FROM readings
                    GROUP BY machine_id
                ) m ON r.machine_id = m.machine_id AND r.id = m.max_id
            )
            SELECT
                latest.*,
                (
                    SELECT COUNT(*)
                    FROM alerts a
                    WHERE a.machine_id = latest.machine_id
                ) AS total_alerts
            FROM latest
            ORDER BY machine_id
            """
        ).fetchall()
    return rows_to_dicts(rows)


def clear_demo_data() -> None:
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM alerts")
        conn.execute("DELETE FROM readings")
        conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('alerts', 'readings')")
