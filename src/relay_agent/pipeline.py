from __future__ import annotations

from pathlib import Path

from . import audit
from .classifier import classify
from .gate import decide
from .models import AgentResult, SupportMessage
from .responder import draft
from .retrieval import TfidfRetriever


class SupportAgent:
    def __init__(self, historical_rows: list[dict[str, str]], audit_path: Path | None = None):
        self.retriever = TfidfRetriever(historical_rows)
        self.audit_path = audit_path

    def handle(self, message: SupportMessage) -> AgentResult:
        evidence = self.retriever.search(message.customer_text)
        intent, confidence = classify(message.customer_text, [item.intent for item in evidence])
        decision, reason = decide(message.customer_text, intent, confidence, evidence)
        result = AgentResult(message.message_id, intent, confidence, draft(intent, evidence), decision, reason, evidence)
        if self.audit_path:
            audit.record(self.audit_path, message, result)
        return result
