from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR
from app.demo_seed import seed_demo_data
from app.processor import process_reading
from app.reset_demo import reset_demo
from app.simulator import generate_reading
from app.storage import (
    export_readings_to_parquet,
    get_machine_status,
    get_recent_alerts,
    get_recent_readings,
    init_db,
)

app = FastAPI(
    title="SmartManuTech IoT Predictive Maintenance",
    description="API para visualizar lecturas IoT, alertas y riesgo predictivo.",
    version="1.0.0",
)

STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/readings")
def readings(limit: int = 100) -> list[dict]:
    return get_recent_readings(limit)


@app.get("/api/alerts")
def alerts(limit: int = 100) -> list[dict]:
    return get_recent_alerts(limit)


@app.get("/api/machines")
def machines() -> list[dict]:
    return get_machine_status()


@app.post("/api/simulate")
def simulate() -> dict:
    reading = generate_reading()
    return process_reading(reading)


@app.post("/api/demo")
def demo() -> dict:
    return seed_demo_data()


@app.post("/api/reset-demo")
def reset_demo_endpoint() -> dict:
    return reset_demo()


@app.post("/api/export/parquet")
def export_parquet() -> dict[str, str]:
    return {"path": export_readings_to_parquet()}
