# Hiver Support Agent

An auditable Python prototype for the Hiver SDE Intern take-home assignment. It classifies an AmazonHelp-style customer message, retrieves similar historical resolutions, drafts a constrained response, and recommends either `auto_handle` or `escalate` with a visible reason.

It is deliberately safe: it never posts a reply, makes account changes, or promises a refund.

## Run in under 5 minutes

Requires Python 3.10+; no packages need to be installed.

```powershell
cd D:\hiver\hiver_support_agent 
$env:PYTHONPATH = "src"
python -m hiver_agent.cli bootstrap-demo
python -m hiver_agent.cli run --text "My package is late and tracking stopped yesterday"
python -m hiver_agent.cli evaluate
```

The last command writes `artifacts/evaluation.json` and `data/audit.sqlite3`.

Run the tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Structure

- `src/hiver_agent/` - retrieval, classifier, escalation gate, responses, audit, and CLI
- `data/demo/` - generated synthetic historical-resolution fixture
- `data/golden/` - generated synthetic 180-row evaluation fixture
- `REPORT.md` - submission report draft
- `PROJECT_REQUIREMENTS.md` - exact assignment mapping and real-data checklist
- `DECISION_LOG.md` - rationale for key implementation choices

## Important submission note

The generated data is only a runnable fixture. Replace it with a documented subsample of the permitted dataset and personally review the golden set before representing it as hand-labelled. See [PROJECT_REQUIREMENTS.md](PROJECT_REQUIREMENTS.md).

## Optional OpenAI judge

After you have a real golden set and independent human reply ratings, you can run an external judge:

```powershell
$env:OPENAI_API_KEY = "your-key"
python -m hiver_agent.cli evaluate --judge openai
```

You must report judge-vs-human agreement, not only the LLM score.
