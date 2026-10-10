# Relay decision log


1. Focused on AmazonHelp so intent definitions and historical language stay brand-specific.
2. Used six intents because small, separable classes are easier to audit than an over-granular taxonomy.
3. Kept `refund_request` and `account_access` escalation-only because safe resolution requires verification outside this prototype.
4. Escalate legal, fraud, safety, discrimination, and threat language regardless of model confidence.
5. Used TF-IDF retrieval to make grounding inspectable and reproducible without an embedding service.
6. Return the retrieved examples in every result rather than hiding retrieval behind a generated answer.
7. Used constrained response templates to prevent unsupported promises such as guaranteed delivery dates or refunds.
8. Logged each result to SQLite to make failures traceable after evaluation.
9. Compared against a trivial all-general-complaint baseline and a keyword-only baseline.
10. Kept the default prototype dependency-free so the reviewer can reproduce it quickly.
11. Separated synthetic demo data from the real-data workflow to avoid misrepresenting demo metrics as benchmark results.
12. Made the offline reply scorer explicitly a proxy rather than calling it an LLM judge.
13. Require human review of golden labels before setting `verified_by_human=true`.
14. Treat auto-handle as a recommendation only; this prototype never sends the reply.
15. Name the reusable project and Python package Relay while keeping the AmazonHelp support workflow as the prototype's dataset context.
