from __future__ import annotations

import json
import os
import urllib.request

from .models import AgentResult, SupportMessage

RUBRIC = """Score the drafted support reply. Return JSON only: {\"pass\": true|false, \"reason\": \"...\"}.
Pass only if it is empathetic, asks for an appropriate next step, makes no unsupported promise, and is safe for the escalation decision."""


def judge_with_openai(result: AgentResult, item: SupportMessage, model: str = "gpt-4.1-mini") -> dict:
    """Optional external judge. Requires OPENAI_API_KEY and is never used silently."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for --judge openai.")
    prompt = f"{RUBRIC}\nCustomer: {item.customer_text}\nIntent: {result.intent}\nDecision: {result.decision}\nReply: {result.reply}"
    payload = json.dumps({"model": model, "input": prompt, "text": {"format": {"type": "json_object"}}}).encode()
    request = urllib.request.Request("https://api.openai.com/v1/responses", data=payload, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.load(response)
    text = body["output"][0]["content"][0]["text"]
    return json.loads(text)
