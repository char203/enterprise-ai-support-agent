import json

from evals.run_eval_v1 import EVAL_FILE

ACTIONS = {"RESOLVE", "REQUEST_INFO", "ESCALATE"}
CATEGORIES = {"Billing", "Account & Access", "Technical", "Product", "Security & Privacy"}


def load_tickets():
    return json.loads(EVAL_FILE.read_text())


def test_tickets_have_required_fields():
    for ticket in load_tickets():
        assert {"id", "ticket", "category", "expected_action"} <= ticket.keys()
        assert ticket["ticket"].strip()


def test_labels_are_valid():
    for ticket in load_tickets():
        assert ticket["expected_action"] in ACTIONS, ticket["id"]
        assert ticket["category"] in CATEGORIES, ticket["id"]


def test_ids_are_unique():
    ids = [ticket["id"] for ticket in load_tickets()]
    assert len(ids) == len(set(ids))
