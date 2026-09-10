from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import AgentResult, SupportMessage


def record(path: Path, message: SupportMessage, result: AgentResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                message_id TEXT PRIMARY KEY, customer_text TEXT NOT NULL, intent TEXT NOT NULL,
                confidence REAL NOT NULL, reply TEXT NOT NULL, decision TEXT NOT NULL,
                decision_reason TEXT NOT NULL, retrieved_json TEXT NOT NULL
            )
        """)
        connection.execute("INSERT OR REPLACE INTO decisions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
            message.message_id, message.customer_text, result.intent, result.confidence,
            result.reply, result.decision, result.decision_reason,
            json.dumps(result.to_dict()["retrieved"]),
        ))
