from __future__ import annotations

from collections import Counter

from .models import AgentResult, SupportMessage
from .pipeline import SupportAgent


def offline_reply_judge(result: AgentResult, item: SupportMessage) -> int:
    """Transparent offline proxy. It is deliberately not represented as an LLM judge."""
    reply = result.reply.lower()
    helpful = "sorry" in reply and "dm" in reply
    safe = not (result.decision == "auto_handle" and item.expected_decision == "escalate")
    aligned = result.intent == item.intent
    return int(helpful and safe and aligned)


def evaluate(agent: SupportAgent, golden: list[SupportMessage]) -> dict:
    outputs = [(item, agent.handle(item)) for item in golden]
    total = len(outputs)
    intent_correct = sum(result.intent == item.intent for item, result in outputs)
    decision_correct = sum(result.decision == item.expected_decision for item, result in outputs)
    judge_scores = [offline_reply_judge(result, item) for item, result in outputs]
    return {
        "examples": total,
        "intent_accuracy": round(intent_correct / total, 3) if total else 0,
        "decision_accuracy": round(decision_correct / total, 3) if total else 0,
        "offline_reply_judge_pass_rate": round(sum(judge_scores) / total, 3) if total else 0,
        "human_verified_examples": sum(item.verified_by_human for item, _ in outputs),
        "intent_distribution": dict(Counter(item.intent for item, _ in outputs)),
        "warning": "Replace this offline proxy with an external LLM judge and validate it against human ratings before submission.",
    }
