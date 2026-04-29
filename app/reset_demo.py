from __future__ import annotations

from app.demo_seed import seed_demo_data
from app.storage import clear_demo_data, export_readings_to_parquet


def reset_demo() -> dict[str, object]:
    clear_demo_data()
    result = seed_demo_data()
    parquet_path = export_readings_to_parquet()
    return {
        **result,
        "parquet_path": parquet_path,
    }


if __name__ == "__main__":
    print(reset_demo())
