from __future__ import annotations

from .models import RetrievedExample

HIGH_RISK_TERMS = {"lawyer", "legal", "sue", "fraud", "police", "scam", "threat", "injured", "unsafe", "discrimination"}
HIGH_RISK_INTENTS = {"refund_request", "account_access"}


def decide(text: str, intent: str, confidence: float, evidence: list[RetrievedExample]) -> tuple[str, str]:
    matched_risk = sorted(term for term in HIGH_RISK_TERMS if term in text.lower())
    if matched_risk:
        return "escalate", f"High-risk language detected: {', '.join(matched_risk)}."
    if intent in HIGH_RISK_INTENTS:
        return "escalate", f"{intent} can require identity or payment verification."
    if confidence < 0.62:
        return "escalate", f"Intent confidence is {confidence:.0%}, below the 62% threshold."
    if not evidence or evidence[0].score < 0.18:
        return "escalate", "No sufficiently similar historical resolution was retrieved."
    return "auto_handle", f"High-confidence {intent} with a similar historical resolution (score {evidence[0].score:.2f})."
