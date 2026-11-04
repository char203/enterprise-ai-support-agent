import json
import re
from pathlib import Path

from src.agent_v1 import analyze_ticket

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVAL_FILE = PROJECT_ROOT / "evals" / "tickets_v1.json"
RESULTS_DIR = PROJECT_ROOT / "results"

# Models often wrap JSON in a ```json ... ``` fence even when told not to.
FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.DOTALL)


def parse_model_output(raw_output: str):
    if not raw_output:
        return None

    match = FENCE.match(raw_output)
    if match:
        raw_output = match.group(1)

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        return None

    return parsed if isinstance(parsed, dict) else None


def run_eval(eval_file=EVAL_FILE, results_dir=RESULTS_DIR):
    tickets = json.loads(Path(eval_file).read_text())

    total = len(tickets)
    if total == 0:
        raise ValueError(f"No tickets found in {eval_file}")
    category_correct = 0
    action_correct = 0
    parse_failures = 0

    results = []

    for item in tickets:
        raw_output = analyze_ticket(item["ticket"])
        parsed = parse_model_output(raw_output)

        if parsed is None:
            parse_failures += 1
            results.append({
                "id": item["id"],
                "ticket": item["ticket"],
                "parse_failure": True,
                "raw_output": raw_output
            })
            continue

        predicted_category = parsed.get("category")
        predicted_action = parsed.get("action")

        category_match = predicted_category == item["category"]
        action_match = predicted_action == item["expected_action"]

        if category_match:
            category_correct += 1

        if action_match:
            action_correct += 1

        results.append({
            "id": item["id"],
            "ticket": item["ticket"],
            "expected_category": item["category"],
            "predicted_category": predicted_category,
            "expected_action": item["expected_action"],
            "predicted_action": predicted_action,
            "category_correct": category_match,
            "action_correct": action_match,
            "confidence": parsed.get("confidence"),
            "reasoning": parsed.get("reasoning"),
            "response": parsed.get("response")
        })

    category_accuracy = category_correct / total
    action_accuracy = action_correct / total

    summary = {
        "total_tickets": total,
        "category_accuracy": category_accuracy,
        "action_accuracy": action_accuracy,
        "parse_failures": parse_failures
    }

    print(json.dumps(summary, indent=2))

    results_dir = Path(results_dir)
    results_dir.mkdir(exist_ok=True)
    (results_dir / "v1_results.json").write_text(
        json.dumps(results, indent=2)
    )

    (results_dir / "v1_summary.json").write_text(
        json.dumps(summary, indent=2)
    )

    return summary


if __name__ == "__main__":
    run_eval()
