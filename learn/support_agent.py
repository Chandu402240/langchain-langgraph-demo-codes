# ---------------------------------------------------------
# AI-Powered Customer Support Agent (Graph like the image)
# Flow:
#   Classify Intent
#      ├── Doc Search ─┐
#      ├── Bug Track ──┼─> Draft Reply ──┬── Human Review (post) ─> END
#      └── Human Review (pre) ───────────┘   └── Send Reply ──────> END
#
# Uses: openai, langchain, langgraph
# Minimal, flat code; FIX: always carry 'email' in state returns and use .get()
# ---------------------------------------------------------

import os, json
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

# -------- Config --------
client = OpenAI()
MODEL = "gpt-4o-mini"  # any Chat Completions-capable model

# -------- Sample Emails (5 required scenarios) --------
sample_emails = [
    "How do I reset my password?",
    "The export feature crashes when I select PDF format.",
    "I was charged twice for my subscription yesterday. Please fix ASAP!",
    "Can you add dark mode to the mobile app?",
    "Our API integration fails intermittently with 504 errors across regions."
]

# =========================================================
# Nodes
# =========================================================

# --- Classify Intent ---
def classify_intent(state):
    email = state.get("email", "")
    system_txt = (
        "You are a routing classifier for customer support.\n"
        "Return strict JSON with keys: intent, urgency, route.\n"
        "- intent ∈ {Account, Billing, Bug, Feature Request, Technical Issue, Other}\n"
        "- urgency ∈ {Low, Medium, High}\n"
        "- route ∈ {doc, bug, human}\n"
        "Routing guidance:\n"
        "- doc: how-to, account/billing questions, feature requests, most FAQs\n"
        "- bug: behavior looks like a product defect or crash\n"
        "- human: legal/safety/security, highly complex, sensitive, or unclear requests\n"
        "No prose. JSON only."
    )
    user_txt = f"Email:\n{email}"
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_txt},
                  {"role": "user", "content": user_txt}],
        temperature=0
    )
    raw = resp.choices[0].message.content.strip()
    data = {"intent":"Other","urgency":"Medium","route":"doc"}
    try:
        data = json.loads(raw)
    except Exception:
        pass
    return {
        "email": email,
        "intent": data.get("intent","Other"),
        "urgency": data.get("urgency","Medium"),
        "route": data.get("route","doc")
    }

# --- Doc Search (simulated) ---
def doc_search(state):
    email = state.get("email", "")
    intent = state.get("intent","Other")
    pt = PromptTemplate.from_template(
        "Pretend to search internal docs for the email below.\n"
        "Return 2-6 short bullets with the most relevant steps or info.\n"
        "Email:\n{email}\nIntent: {intent}"
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": pt.format(email=email, intent=intent)}],
        temperature=0.2
    )
    notes = resp.choices[0].message.content.strip()
    return {"email": email, "kb_notes": notes}

# --- Bug Track (simulated ticketing) ---
def bug_track(state):
    email = state.get("email", "")
    pt = PromptTemplate.from_template(
        "Create a concise bug intake summary from the email.\n"
        "Respond in JSON with keys: title, suspected_area, severity (Low|Med|High), "
        "needed_info (short list), suggested_workaround.\n"
        "Email:\n{email}"
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": pt.format(email=email)}],
        temperature=0.2
    )
    raw = resp.choices[0].message.content.strip()
    try:
        bug = json.loads(raw)
    except Exception:
        bug = {
            "title":"Bug report",
            "suspected_area":"Unknown",
            "severity":"Med",
            "needed_info":["steps to reproduce","timestamp","logs"],
            "suggested_workaround":"None"
        }
    return {"email": email, "bug_notes": json.dumps(bug)}

# --- Human Review (pre-draft) ---
def human_review_pre(state):
    email = state.get("email", "")
    reason = "Complex or sensitive case selected at classification."
    return {"email": email, "escalate": "Yes", "human_review_notes_pre": reason}

# --- Draft Reply ---
def draft_reply(state):
    email = state.get("email", "")
    intent = state.get("intent","Other")
    urgency = state.get("urgency","Medium")
    kb = state.get("kb_notes","")
    bug_notes = state.get("bug_notes","")
    escalate = state.get("escalate","No")

    system_txt = (
        "You are a professional support agent. Write a concise, empathetic reply (~150 words).\n"
        "- Use intent/urgency and any KB or bug notes.\n"
        "- Billing: acknowledge urgency, explain next steps clearly.\n"
        "- Bug: ask for missing repro info, offer workaround if present.\n"
        "- Account/how-to: give clear step-by-step.\n"
        "- Feature request: acknowledge and set expectations.\n"
        "- If escalate=='Yes', mention that a specialist will review.\n"
        "Ask 1-2 specific clarifying questions only if needed. Do not invent facts."
    )
    user_txt = (
        f"Email:\n{email}\n\n"
        f"Intent: {intent}\nUrgency: {urgency}\n"
        f"KB Notes:\n{kb}\n\nBug Notes:\n{bug_notes}\n"
        f"Escalate Flag: {escalate}"
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_txt},
                  {"role": "user", "content": user_txt}],
        temperature=0.3
    )
    draft = resp.choices[0].message.content.strip()

    should_escalate = (
        (state.get("escalate","No") == "Yes") or
        (intent in ["Bug","Technical Issue"] and urgency == "High")
    )
    return {
        "email": email,
        "draft_reply": draft,
        "escalate_after_draft": "Yes" if should_escalate else "No"
    }

# --- Human Review (post-draft) ---
def human_review_post(state):
    email = state.get("email", "")
    draft = state.get("draft_reply","")
    intent = state.get("intent","Other")
    urgency = state.get("urgency","Medium")
    pt = PromptTemplate.from_template(
        "You are the human-triage assistant. Summarize why this needs human review "
        "and which team should handle it (Billing, Support, Engineering). "
        "Reply in JSON with keys: reason, assignee_team, priority.\n\n"
        "Email:\n{email}\n\nDraft:\n{draft}\nIntent: {intent}\nUrgency: {urgency}"
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": pt.format(email=email, draft=draft, intent=intent, urgency=urgency)}],
        temperature=0
    )
    raw = resp.choices[0].message.content.strip()
    try:
        review = json.loads(raw)
    except Exception:
        review = {"reason":"Complex case", "assignee_team":"Support", "priority":"P2"}
    return {
        "email": email,
        "final_action": "Escalate to Human",
        "human_review_summary": json.dumps(review)
    }

# --- Send Reply ---
def send_reply(state):
    email = state.get("email", "")
    # In real usage, send email here.
    return {"email": email, "final_action": "Auto-Reply Sent"}

# =========================================================
# Graph wiring to match the diagram
# =========================================================

graph = StateGraph(dict)  # simple dict state

graph.add_node("classify_intent", classify_intent)
graph.add_node("doc_search", doc_search)
graph.add_node("bug_track", bug_track)
graph.add_node("human_review_pre", human_review_pre)
graph.add_node("draft_reply", draft_reply)
graph.add_node("human_review_post", human_review_post)
graph.add_node("send_reply", send_reply)

# Entry
graph.set_entry_point("classify_intent")

# From Classify -> (Doc | Bug | Human pre)
def route_from_classify(state):
    return state.get("route","doc")

graph.add_conditional_edges(
    "classify_intent",
    route_from_classify,
    {
        "doc": "doc_search",
        "bug": "bug_track",
        "human": "human_review_pre"
    }
)

# Converge to Draft Reply
graph.add_edge("doc_search", "draft_reply")
graph.add_edge("bug_track", "draft_reply")
graph.add_edge("human_review_pre", "draft_reply")

# From Draft Reply -> (Human post | Send Reply)
def route_after_draft(state):
    return "human" if state.get("escalate_after_draft","No") == "Yes" else "send"

graph.add_conditional_edges(
    "draft_reply",
    route_after_draft,
    {
        "human": "human_review_post",
        "send": "send_reply"
    }
)

# Both branches end
graph.add_edge("human_review_post", END)
graph.add_edge("send_reply", END)

app = graph.compile()

# =========================================================
# Run on the 5 sample scenarios & print results
# =========================================================
for i, email_text in enumerate(sample_emails, start=1):
    print("\n" + "="*78)
    print(f"SCENARIO {i}")
    print("="*78)
    result = app.invoke({"email": email_text})
    print("EMAIL INPUT:\n", email_text)

    print("\n— Classification —")
    print("Intent:", result.get("intent"))
    print("Urgency:", result.get("urgency"))
    print("Route:", result.get("route"))

    if "kb_notes" in result:
        print("\n— Doc Search Notes —\n", result.get("kb_notes"))
    if "bug_notes" in result:
        print("\n— Bug Track —\n", result.get("bug_notes"))
    if "human_review_notes_pre" in result:
        print("\n— Human Review (pre) —\n", result.get("human_review_notes_pre"))

    print("\n— Draft Reply —\n", result.get("draft_reply"))

    if result.get("final_action") == "Escalate to Human":
        print("\n— Human Review (post) —\n", result.get("human_review_summary"))

    print("\n— Final Action —\n", result.get("final_action"))