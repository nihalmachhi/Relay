from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SupportMessage:
    message_id: str
    customer_text: str
    brand: str
    intent: str | None = None
    expected_reply: str | None = None
    expected_decision: str | None = None
    verified_by_human: bool = False


@dataclass(frozen=True)
class RetrievedExample:
    message_id: str
    customer_text: str
    agent_reply: str
    intent: str
    score: float


@dataclass(frozen=True)
class AgentResult:
    message_id: str
    intent: str
    confidence: float
    reply: str
    decision: str
    decision_reason: str
    retrieved: list[RetrievedExample]

    def to_dict(self) -> dict:
        value = asdict(self)
        value["retrieved"] = [asdict(item) for item in self.retrieved]
        return value
