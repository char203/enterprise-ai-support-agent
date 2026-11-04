from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = PROJECT_ROOT / "knowledge_base"

MODEL = "gpt-5.4-mini"

_client = None


def get_client():
    # Created lazily so the module can be imported (e.g. by tests) without
    # an OPENAI_API_KEY in the environment.
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def load_knowledge_base():
    documents = []

    # Sorted so the prompt is identical across runs and machines.
    for path in sorted(KB_DIR.glob("*.md")):
        documents.append(
            f"### {path.stem}\n{path.read_text()}"
        )

    return "\n\n".join(documents)


def build_prompt(ticket: str, knowledge_base: str):
    return f"""
You are a customer support agent for Relay, a B2B SaaS company.

Use ONLY the company policies below when making decisions.
Do not invent company policies or troubleshooting instructions.

Possible categories:
- Billing
- Account & Access
- Technical
- Product
- Security & Privacy

Possible actions:
- RESOLVE
- ESCALATE
- REQUEST_INFO

COMPANY POLICIES:

{knowledge_base}

CUSTOMER TICKET:

{ticket}

Return JSON with exactly these fields:

category
action
confidence
reasoning
response

confidence must be a number between 0 and 1.
"""


def analyze_ticket(ticket: str):
    prompt = build_prompt(ticket, load_knowledge_base())

    response = get_client().responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":
    test_ticket = "I was charged twice this month."

    result = analyze_ticket(test_ticket)

    print(result)
