from __future__ import annotations

import argparse
import json
from pathlib import Path

from .data import read_golden, read_historical
from .demo import bootstrap
from .evaluate import evaluate
from .models import SupportMessage
from .pipeline import SupportAgent


def root_from_args(value: str | None) -> Path:
    return Path(value).resolve() if value else Path(__file__).resolve().parents[2]


def make_agent(root: Path) -> SupportAgent:
    history = read_historical(root / "data/demo/historical_resolutions.csv", "AmazonHelp")
    return SupportAgent(history, root / "data/audit.sqlite3")


def baseline_scores(golden: list[SupportMessage]) -> dict:
    # Trivial baseline: every issue is a generic complaint and gets escalated.
    trivial_intent = sum(item.intent == "general_complaint" for item in golden) / len(golden)
    trivial_decision = sum(item.expected_decision == "escalate" for item in golden) / len(golden)
    # Simple baseline: keyword-only intent (no retrieval) and conservative escalation.
    from .classifier import classify
    keyword_correct = sum(classify(item.customer_text, [])[0] == item.intent for item in golden) / len(golden)
    return {"trivial_intent_accuracy": round(trivial_intent, 3), "trivial_decision_accuracy": round(trivial_decision, 3), "keyword_only_intent_accuracy": round(keyword_correct, 3)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the auditable support-agent prototype.")
    parser.add_argument("command", choices=["bootstrap-demo", "run", "evaluate"])
    parser.add_argument("--root", help="Project root; defaults to repository root")
    parser.add_argument("--text", help="Incoming customer message for the run command")
    parser.add_argument("--judge", choices=["offline", "openai"], default="offline", help="Reply-quality judge used for evaluation")
    arguments = parser.parse_args()
    root = root_from_args(arguments.root)
    if arguments.command == "bootstrap-demo":
        bootstrap(root)
        print(json.dumps({"created": ["data/demo/historical_resolutions.csv", "data/golden/golden_set.csv"], "note": "Synthetic demo data only; review golden labels against the real Kaggle subsample before submission."}, indent=2))
        return
    if not (root / "data/demo/historical_resolutions.csv").exists():
        raise SystemExit("Run `python -m relay_agent.cli bootstrap-demo` first.")
    agent = make_agent(root)
    if arguments.command == "run":
        if not arguments.text:
            raise SystemExit("`run` requires --text.")
        message = SupportMessage("interactive-1", arguments.text, "AmazonHelp")
        print(json.dumps(agent.handle(message).to_dict(), indent=2))
        return
    golden = read_golden(root / "data/golden/golden_set.csv", "AmazonHelp")
    results = evaluate(agent, golden) | {"baselines": baseline_scores(golden)}
    if arguments.judge == "openai":
        from .llm_judge import judge_with_openai
        scores = [judge_with_openai(agent.handle(item), item) for item in golden]
        results["openai_judge_pass_rate"] = round(sum(bool(score.get("pass")) for score in scores) / len(scores), 3)
        results["openai_judge_note"] = "Compare these scores against independently collected human labels before reporting agreement."
    output = root / "artifacts/evaluation.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"\nSaved {output}")


if __name__ == "__main__":
    main()
