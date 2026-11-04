# Enterprise AI Support Agent

[![CI](https://github.com/char203/enterprise-ai-support-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/char203/enterprise-ai-support-agent/actions/workflows/ci.yml)

**Relay AI Customer Support Triage Agent** — a portfolio project for a fictional B2B SaaS company ("Relay").

Workflow: Incoming ticket → Understand → Classify → Investigate → Consult policy → Decide action → RESOLVE / ESCALATE / REQUEST_INFO → Respond → Document

An AI-powered customer support workflow for a fictional B2B SaaS company, designed to classify tickets, route actions, generate policy-grounded responses, and escalate high-risk cases to humans.

## What it does

- Classifies support tickets across 5 workflows
- Chooses between RESOLVE, REQUEST_INFO, and ESCALATE
- Grounds responses in internal policy documents
- Measures policy adherence, routing accuracy, hallucinations, and escalation behavior
- Evaluates human-in-the-loop safety for high-risk security cases

## Evaluation

Current V1 results:
- 86% policy adherence
- 90% escalation recall on critical security cases
- 20% estimated reduction in manual ticket-handling time

## Tech Stack

Python, OpenAI API, JSON structured outputs, LLM evaluation

## Getting Started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
echo "OPENAI_API_KEY=sk-..." > .env

python -m src.agent_v1          # classify a single sample ticket
python -m evals.run_eval_v1     # run the evaluation; writes results/v1_*.json
pytest                          # offline unit tests (no API key needed)
```

Run commands from the repository root.

## Project Structure

- `src/` — agent logic
- `knowledge_base/` — company policies
- `evals/` — ground-truth test cases and evaluation harness
- `results/` — local evaluation outputs
- `tests/` — offline unit tests for parsing, scoring, and dataset validity

## Why I built this

