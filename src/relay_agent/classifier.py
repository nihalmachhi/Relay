from __future__ import annotations

from collections import Counter

from .retrieval import tokens

INTENTS = ("delivery_delay", "refund_request", "account_access", "damaged_item", "order_status", "general_complaint")

KEYWORDS = {
    "delivery_delay": {"late", "delay", "delayed", "delivery", "arrive", "arrived", "shipping", "shipped"},
    "refund_request": {"refund", "return", "money", "charged", "charge", "cancel"},
    "account_access": {"account", "login", "password", "locked", "sign", "access"},
    "damaged_item": {"damaged", "broken", "defective", "wrong", "missing", "item"},
    "order_status": {"order", "track", "tracking", "status", "where", "package"},
    "general_complaint": {"bad", "terrible", "awful", "unhappy", "disappointed", "help"},
}


def classify(text: str, retrieved_intents: list[str]) -> tuple[str, float]:
    message_tokens = set(tokens(text))
    scores = {intent: len(message_tokens & words) for intent, words in KEYWORDS.items()}
    for intent, count in Counter(retrieved_intents).items():
        scores[intent] = scores.get(intent, 0) + count * 0.35
    best = max(scores, key=scores.get)
    ranked = sorted(scores.values(), reverse=True)
    margin = ranked[0] - ranked[1] if len(ranked) > 1 else ranked[0]
    confidence = min(0.95, 0.4 + scores[best] * 0.15 + margin * 0.08)
    return best, round(confidence, 2)
