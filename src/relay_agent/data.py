from __future__ import annotations

import csv
from pathlib import Path

from .models import SupportMessage

HISTORICAL_FIELDS = ["message_id", "brand", "customer_text", "agent_reply", "intent"]
GOLDEN_FIELDS = [
    "message_id", "brand", "customer_text", "intent", "expected_reply",
    "expected_decision", "verified_by_human",
]


def read_historical(path: Path, brand: str) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = set(HISTORICAL_FIELDS)
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"{path} must contain: {', '.join(HISTORICAL_FIELDS)}")
    return [row for row in rows if row["brand"].lower() == brand.lower()]


def read_golden(path: Path, brand: str) -> list[SupportMessage]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not set(GOLDEN_FIELDS).issubset(rows[0]):
        raise ValueError(f"{path} must contain: {', '.join(GOLDEN_FIELDS)}")
    return [
        SupportMessage(
            message_id=row["message_id"], customer_text=row["customer_text"], brand=row["brand"],
            intent=row["intent"], expected_reply=row["expected_reply"],
            expected_decision=row["expected_decision"],
            verified_by_human=row["verified_by_human"].strip().lower() == "true",
        )
        for row in rows if row["brand"].lower() == brand.lower()
    ]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
