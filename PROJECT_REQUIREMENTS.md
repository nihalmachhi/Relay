# Relay support-agent project requirements

This repository implements the assignment as an AmazonHelp-focused prototype.

## Product scope

Input: one incoming customer-support message. Output: a defined intent, a conservative draft reply, an auto-handle/escalate decision, its reason, and the closest historical examples used as evidence.

The system intentionally does not send messages, access customer accounts, process refunds, or claim to resolve a case. Payment/account/refund topics and legal/safety signals always escalate.

## Assignment mapping

| Assignment requirement | Repository implementation |
| --- | --- |
| Runnable pipeline | `python -m relay_agent.cli run --text "..."` |
| Golden set | `data/golden/golden_set.csv`; must be human-reviewed before submission |
| Metrics + two baselines | `python -m relay_agent.cli evaluate` |
| Grounded replies | TF-IDF retrieval stores the three closest historical resolutions |
| Escalation reason | `src/relay_agent/gate.py` and the SQLite audit log |
| LLM-as-judge | Optional `--judge openai` extension in `llm_judge.py`; validate it against human scores before reporting |
| Decision log/report | `DECISION_LOG.md` and `REPORT.md` |

## Real-data replacement checklist

1. Download the permitted Kaggle Customer Support on Twitter data yourself and document its version/date.
2. Create a reproducible brand-specific subsample and export historical resolved examples using the CSV columns in `src/relay_agent/data.py`.
3. Replace the synthetic demo files. Label 150-250 examples independently; set `verified_by_human=true` only after a real review.
4. Run evaluation, use the real metrics in `REPORT.md`, and preserve the resulting `artifacts/evaluation.json`.
5. Score a stratified subset of reply outputs yourself, then compare the optional LLM judge to those human pass/fail labels. Do not state an LLM judge agreement number until that experiment has been run.
