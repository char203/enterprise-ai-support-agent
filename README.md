# Relay AI Customer Support Triage Agent

A portfolio project for a fictional B2B SaaS company ("Relay").

Workflow:
Incoming ticket -> Understand -> Classify -> Investigate -> Consult policy ->
Decide action -> RESOLVE / ESCALATE / REQUEST_INFO -> Respond -> Document

This bundle reconstructs the project files created in our conversation so far.
The 20-ticket evaluation dataset was created by the user locally but its exact
contents were not shared in chat, so `evals/tickets_v1.json` contains the four
examples explicitly established in the conversation plus a note explaining the gap.
Likewise, no actual V1 evaluation output was shared, so the `results/` files are
placeholders rather than fabricated metrics.
# Enterprise AI Support Agent

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

## Project Structure

- `src/` — agent logic
- `knowledge_base/` — company policies
- `evals/` — ground-truth test cases and evaluation harness
- `results/` — local evaluation outputs

## Why I built this

I wanted to understand what it takes to move from a simple LLM demo to a more production-oriented enterprise AI workflow: defining ground truth, evaluating reliability, handling ambiguous cases, and deciding when a human should stay in the loop.