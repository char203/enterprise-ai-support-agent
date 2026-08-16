import json
from pathlib import Path

from src.agent_v1 import analyze_ticket

EVAL_FILE = Path("evals/tickets_v1.json")


def parse_model_output(raw_output: str):
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return None


def run_eval():
    tickets = json.loads(EVAL_FILE.read_text())

    total = len(tickets)
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

    Path("results").mkdir(exist_ok=True)
    Path("results/v1_results.json").write_text(
        json.dumps(results, indent=2)
    )

    Path("results/v1_summary.json").write_text(
        json.dumps(summary, indent=2)
    )


if __name__ == "__main__":
    run_eval()
