from __future__ import annotations

from .models import RetrievedExample

TEMPLATES = {
    "delivery_delay": "Sorry your delivery has not arrived as expected. Please send your order number by DM so our team can check the latest delivery status.",
    "refund_request": "Sorry about this. For your security, please contact our support team by DM with your order details so they can review the refund request.",
    "account_access": "Sorry you are having trouble accessing your account. Please contact support by DM so we can verify the account safely and help restore access.",
    "damaged_item": "Sorry your item was not received in the expected condition. Please send your order number and a photo by DM so our team can review the replacement options.",
    "order_status": "We can help check this. Please send your order number by DM and our team will look up the latest tracking information.",
    "general_complaint": "Sorry that your experience has been frustrating. Please send us the relevant order details by DM so our team can investigate and help.",
}


def draft(intent: str, evidence: list[RetrievedExample]) -> str:
    """A constrained template avoids unsupported promises; evidence remains auditable."""
    return TEMPLATES[intent]
