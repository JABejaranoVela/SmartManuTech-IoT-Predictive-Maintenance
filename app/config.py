from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "smartmanutech.db"

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "iot-machine-readings"

MACHINE_IDS = ["SMT-01", "SMT-02", "SMT-03", "SMT-04"]
