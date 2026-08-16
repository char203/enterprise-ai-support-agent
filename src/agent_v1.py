from dotenv import load_dotenv
load_dotenv()

import json
from pathlib import Path
from openai import OpenAI

client = OpenAI()

KB_DIR = Path("knowledge_base")

def load_knowledge_base():
    documents = []

    for path in KB_DIR.glob("*.md"):
        documents.append(
            f"### {path.stem}\n{path.read_text()}"
        )

    return "\n\n".join(documents)


def analyze_ticket(ticket: str):
    knowledge_base = load_knowledge_base()

    prompt = f"""
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

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":
    test_ticket = "I was charged twice this month."

    result = analyze_ticket(test_ticket)

    print(result)
