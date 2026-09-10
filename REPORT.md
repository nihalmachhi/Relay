# Hiver SDE Intern Assignment - report draft

> Replace every `[TODO]` with results from the real Kaggle subsample. Do not submit the synthetic-demo numbers.

## Problem framing

This project handles public AmazonHelp-style customer messages. Good means: predict a useful high-level intent, produce a reply that is empathetic and follows a historically observed support pattern, and avoid unsafe automation. The agent can recommend a draft but never sends it.

Out of scope: account verification, refunds, private data collection, transaction updates, multilingual support, and final case resolution.

## System

The pipeline retrieves similar resolved messages with TF-IDF, classifies the intent from message keywords plus retrieval votes, uses a constrained intent-specific draft, and applies a conservative escalation gate. Every output stores its evidence and decision reason in SQLite.

## Evaluation protocol

Sample `[TODO: N]` AmazonHelp customer messages from the downloaded dataset. Create a 150-250 row golden set using a documented sampling strategy. Label intent, expected escalation decision, and reply-quality pass/fail independently from the system output. Split historical retrieval examples and golden examples by conversation/thread to avoid leakage.

Metrics: intent accuracy, decision accuracy, reply-quality pass rate, and false auto-handle rate. Compare with (1) a trivial all-complaint/escalate baseline and (2) a keyword-only no-retrieval baseline.

| System | Intent accuracy | Decision accuracy | Reply pass rate |
| --- | ---: | ---: | ---: |
| Trivial baseline | [TODO] | [TODO] | [TODO] |
| Keyword baseline | [TODO] | [TODO] | [TODO] |
| Retrieval + gate | [TODO] | [TODO] | [TODO] |

## LLM judge validation

Score a stratified sample of `[TODO]` system outputs with the defined rubric and independently score the same outputs by hand. Report agreement, disagreement examples, and the human score. An LLM score alone is not treated as ground truth.

## Top failure modes to investigate

1. Overlapping terms: “charged” can mean a refund dispute or a delivery fee.
2. Missing context: a tweet may reference a prior message not in the single-message input.
3. Lexical mismatch: TF-IDF may miss semantically similar but differently worded messages.
4. Generic replies: constrained templates can be safe but less personally helpful.
5. Escalation calibration: conservative thresholds may burden humans; lower thresholds can create unsafe auto-handles.

## What is misleading about the headline number?

The intent accuracy can be inflated by templated or frequent intents, while the operational cost is dominated by rare, high-risk messages. It also does not measure whether an auto-handled reply was actually correct, timely, or acceptable to a customer. Report per-intent counts, false auto-handle rate, and human-reviewed reply quality beside any overall accuracy.

## One more week

Use conversation threads rather than isolated tweets, replace TF-IDF with an evaluated embedding retriever, add calibrated confidence estimates, annotate more difficult rare cases, and run a blinded human evaluation of draft usefulness and escalation safety.
