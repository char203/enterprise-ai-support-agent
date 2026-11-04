from src import agent_v1


def test_knowledge_base_includes_every_policy_file():
    kb = agent_v1.load_knowledge_base()
    for name in ["account_access", "billing", "product", "security_privacy", "technical"]:
        assert f"### {name}" in kb


def test_knowledge_base_is_deterministic():
    assert agent_v1.load_knowledge_base() == agent_v1.load_knowledge_base()
    headings = [line for line in agent_v1.load_knowledge_base().splitlines() if line.startswith("### ")]
    assert headings == sorted(headings)


def test_prompt_contains_ticket_and_policies():
    prompt = agent_v1.build_prompt("I was charged twice.", "### billing\nRefunds above $500 ...")
    assert "I was charged twice." in prompt
    assert "Refunds above $500" in prompt
    for action in ["RESOLVE", "ESCALATE", "REQUEST_INFO"]:
        assert action in prompt
