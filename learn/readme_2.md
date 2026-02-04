# AI-Powered Customer Support Agent (LangGraph)

Minimal workflow aligned to the diagram:

    Classify Intent
       ├── Doc Search ─┐
       ├── Bug Track ──┼─> Draft Reply ──┬── Human Review (post) ─> END
       └── Human Review (pre) ───────────┘   └── Send Reply ──────> END

## What it does

*   Classifies **intent** (Account, Billing, Bug, Feature Request, Technical Issue, Other) and **urgency** (Low/Medium/High).
*   Routes to **Doc Search** (simulated), **Bug Track** (intake JSON), or **Human Review (pre)**.
*   Generates a concise, empathetic **draft reply**.
*   Decides **Send Reply** vs **Human Review (post)** and ends.

## Why it’s robust

*   Each node uses `state.get(...)` and **returns `"email"`** to avoid `KeyError: 'email'` and preserve state across nodes.

## Requirements

```bash
python >= 3.9
pip install openai langchain langgraph
# set your OpenAI key
export OPENAI_API_KEY="your_key_here"   # macOS/Linux
# setx OPENAI_API_KEY "your_key_here"   # Windows PowerShell
```

## Run

```bash
python support_agent_graph.py
```

## Sample scenarios included

1.  Reset password (how‑to)
2.  Export to PDF crashes (bug)
3.  Charged twice (billing, urgent)
4.  Dark mode (feature request)
5.  Intermittent 504s (complex tech)

## Key nodes (plain English)

*   **classify\_intent** → outputs `{intent, urgency, route}` with `route ∈ {doc, bug, human}`.
*   **doc\_search** → returns bullet **kb\_notes** (LLM‑simulated RAG).
*   **bug\_track** → returns **bug\_notes** JSON (title, area, severity, needed\_info, workaround).
*   **human\_review\_pre** → sets `escalate=Yes` for complex/sensitive items.
*   **draft\_reply** → composes the customer email and sets `escalate_after_draft`.
*   **human\_review\_post** → JSON summary `{reason, assignee_team, priority}`.
*   **send\_reply** → simulates sending the email.

## Outputs printed per scenario

*   Intent, Urgency, Route
*   Doc/Bug/Human‑pre details (as applicable)
*   Draft reply
*   Final action: **Auto‑Reply Sent** or **Escalate to Human**
*   If escalated: Human review summary JSON

## Customize quickly

*   **Model**: change `MODEL = "gpt-4o-mini"` to any chat‑completions model you have.
*   **Doc Search**: swap simulated notes for real RAG.
*   **Send Reply**: call your email/CRM API.
*   **Bug Track**: create real tickets (Jira, Linear, etc.).
*   **Escalation policy**: adjust the heuristic inside `draft_reply`.

## Tips & Troubleshooting

*   If routing feels loose, tighten prompts or add rule overrides after `classify_intent`.
*   Authentication errors: ensure `OPENAI_API_KEY` is set in the environment.
*   For auditable runs, write `result` dicts to JSON files.

## Project structure (suggested)

    support-agent/
    ├─ support_agent_graph.py
    └─ README.md

