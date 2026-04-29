from __future__ import annotations

from app.demo_seed import seed_demo_data
from app.storage import clear_demo_data


def reset_demo() -> dict[str, object]:
    clear_demo_data()
    return seed_demo_data()


if __name__ == "__main__":
    print(reset_demo())
