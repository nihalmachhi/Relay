from __future__ import annotations

from pathlib import Path

from .data import GOLDEN_FIELDS, HISTORICAL_FIELDS, write_csv

EXAMPLES = {
    "delivery_delay": [("My delivery is late again, where is it?", "Sorry your delivery has not arrived as expected. Please send your order number by DM so our team can check the latest delivery status."), ("Package was due yesterday and tracking has stopped", "Sorry for the delay. Please DM your order number and we will check the latest delivery update.")],
    "refund_request": [("I need a refund for the cancelled order", "Sorry about this. Please DM your order details so our team can review your refund request."), ("Why was I charged after I returned this?", "Please send the order details by DM and our team will review the charge and return." )],
    "account_access": [("My account is locked and I cannot login", "Sorry you cannot access your account. Please DM us so we can help verify and restore access."), ("Password reset does not work", "Please contact us by DM so our team can safely help with your account access." )],
    "damaged_item": [("My item arrived broken", "Sorry your item arrived damaged. Please send your order number and a photo by DM so we can review replacement options."), ("The package has the wrong item inside", "Sorry about the incorrect item. Please DM your order details and a photo so we can help." )],
    "order_status": [("Can you track my order please?", "Please send your order number by DM and we will check the latest tracking information."), ("Where is my package right now?", "We can help check the delivery status. Please DM the order number." )],
    "general_complaint": [("This support experience has been terrible", "Sorry this experience has been frustrating. Please DM the details so our team can investigate."), ("I am very disappointed with this service", "Sorry to hear this. Please DM the relevant order details so we can help." )],
}


def bootstrap(root: Path) -> None:
    historical, golden = [], []
    number = 1
    for intent, rows in EXAMPLES.items():
        for text, reply in rows:
            historical.append({"message_id": f"history-{number}", "brand": "AmazonHelp", "customer_text": text, "agent_reply": reply, "intent": intent})
            number += 1
    # Repeat with natural text variants to make the runnable demo eval set 180 rows.
    for index in range(180):
        intent = list(EXAMPLES)[index % len(EXAMPLES)]
        text, reply = EXAMPLES[intent][(index // len(EXAMPLES)) % len(EXAMPLES[intent])]
        suffix = (" I have already checked tracking." if index % 5 == 0 else " Please help.")
        expected = "escalate" if intent in {"refund_request", "account_access"} else "auto_handle"
        golden.append({"message_id": f"gold-{index + 1:03d}", "brand": "AmazonHelp", "customer_text": text + suffix, "intent": intent, "expected_reply": reply, "expected_decision": expected, "verified_by_human": "false"})
    write_csv(root / "data" / "demo" / "historical_resolutions.csv", HISTORICAL_FIELDS, historical)
    write_csv(root / "data" / "golden" / "golden_set.csv", GOLDEN_FIELDS, golden)
