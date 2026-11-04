import json

import pytest

from evals import run_eval_v1
from evals.run_eval_v1 import parse_model_output


def test_parse_plain_json():
    assert parse_model_output('{"action": "ESCALATE"}') == {"action": "ESCALATE"}


def test_parse_fenced_json():
    raw = '```json\n{"action": "RESOLVE", "category": "Product"}\n```'
    assert parse_model_output(raw) == {"action": "RESOLVE", "category": "Product"}


@pytest.mark.parametrize("raw", ["", None, "not json", "[1, 2]", '"ESCALATE"'])
def test_parse_rejects_non_objects(raw):
    assert parse_model_output(raw) is None


def write_tickets(tmp_path, tickets):
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(tickets))
    return path


def test_run_eval_scores_and_writes_results(tmp_path, monkeypatch):
    tickets = [
        {"id": 1, "ticket": "a", "category": "Billing", "expected_action": "REQUEST_INFO"},
        {"id": 2, "ticket": "b", "category": "Product", "expected_action": "RESOLVE"},
        {"id": 3, "ticket": "c", "category": "Technical", "expected_action": "ESCALATE"},
    ]
    outputs = {
        "a": '{"category": "Billing", "action": "REQUEST_INFO"}',
        "b": '```json\n{"category": "Billing", "action": "RESOLVE"}\n```',
        "c": "Sorry, I can't help with that.",
    }
    monkeypatch.setattr(run_eval_v1, "analyze_ticket", outputs.__getitem__)

    summary = run_eval_v1.run_eval(write_tickets(tmp_path, tickets), tmp_path / "out")

    assert summary == {
        "total_tickets": 3,
        "category_accuracy": 1 / 3,
        "action_accuracy": 2 / 3,
        "parse_failures": 1,
    }
    results = json.loads((tmp_path / "out" / "v1_results.json").read_text())
    assert results[2]["parse_failure"] is True


def test_run_eval_rejects_empty_dataset(tmp_path, monkeypatch):
    monkeypatch.setattr(run_eval_v1, "analyze_ticket", lambda t: "{}")
    with pytest.raises(ValueError):
        run_eval_v1.run_eval(write_tickets(tmp_path, []), tmp_path / "out")
