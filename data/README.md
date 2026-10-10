# Data folders

This repository includes small synthetic fixtures so the CLI and evaluation pipeline can run without downloading a dataset. They are examples for development only; the generated golden labels are not human reviewed and their scores are not evidence of production performance.

## `demo/`

`historical_resolutions.csv` contains 12 synthetic examples. The retriever uses `customer_text`, `agent_reply`, and `intent` to find similar cases and provide evidence for a draft.

Columns: `message_id`, `brand`, `customer_text`, `agent_reply`, `intent`.

## `golden/`

`golden_set.csv` contains 180 generated evaluation examples. `verified_by_human` is `false` for every generated row. Review and label a real, permitted sample independently before using these fields as benchmark truth.

Columns: `message_id`, `brand`, `customer_text`, `intent`, `expected_reply`, `expected_decision`, `verified_by_human`.

Run `python -m relay_agent.cli bootstrap-demo` from the repository root to regenerate both fixtures. Before formal evaluation, replace them with a documented, permitted data sample, review labels independently, and avoid sharing conversations between retrieval and evaluation sets.
