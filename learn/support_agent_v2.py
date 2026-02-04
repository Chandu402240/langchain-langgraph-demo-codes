# ---------------------------------------------------------
# SIMPLE AI CUSTOMER SUPPORT AGENT USING:
# openai, langchain, langgraph
# ---------------------------------------------------------

from openai import OpenAI
#from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph as Graph, END

# ---------------------------------------
# 0. API Client
# ---------------------------------------
client = OpenAI()

llm = client.chat.completions.create(model="gpt-4o-mini")

# ---------------------------------------
# 1. Sample incoming email (you can edit this)
# ---------------------------------------
email_text = """
Hi team, the export feature crashes whenever I choose PDF format.
Please fix this ASAP.
"""

# ---------------------------------------
# 2. Small mock knowledge base
# ---------------------------------------
knowledge_base = {
    "password reset": "To reset your password, go to Settings → Security → Reset Password.",
    "export pdf crash": "This is a known bug. A fix is being rolled out in the next patch.",
    "double billing": "Duplicate charges are usually reversed automatically in 3–5 business days.",
}

# ---------------------------------------
# 3. Build a simple LangGraph pipeline
# ---------------------------------------

graph = Graph()

# ---- Node 1: classify urgency + topic ----
def classify_email(state):
    prompt = f"""
    Classify the urgency and topic of this email:

    Email:
    {state['email']}

    Urgency options: Low, Medium, High
    Topic options: Account, Billing, Bug, Feature Request, Technical Issue

    Return JSON with:
    urgency:
    topic:
    """
    result = llm.call(prompt)
    state["classification"] = result
    return state

# ---- Node 2: search knowledge base ----
def search_docs(state):
    email = state["email"].lower()
    found = "No relevant documentation found."

    for key, value in knowledge_base.items():
        if key in email:
            found = value
            break

    state["kb_result"] = found
    return state

# ---- Node 3: generate draft response ----
def generate_response(state):
    prompt = f"""
    Email from customer:
    {state['email']}

    Classification:
    {state['classification']}

    Knowledge base result:
    {state['kb_result']}

    Write a helpful customer support reply.
    """
    result = llm.call(prompt)
    state["draft"] = result
    return state

# ---- Node 4: Decide auto‑reply vs escalation ----
def decision_logic(state):
    urgency_check = "High" in state["classification"]
    unresolved = "No relevant documentation" in state["kb_result"]

    if urgency_check or unresolved:
        decision = "ESCALATE_TO_HUMAN"
    else:
        decision = "AUTO_REPLY"

    state["decision"] = decision
    return state

# ---- Node 5: Follow‑up handling ----
def follow_up_logic(state):
    if "known bug" in state["kb_result"].lower():
        state["follow_up"] = "Schedule follow‑up: notify customer when bug is fixed."
    else:
        state["follow_up"] = "No follow‑up needed."

    return state


# ---------------------------------------
# Add nodes to graph
# ---------------------------------------
graph.add_node("classify", classify_email)
graph.add_node("search", search_docs)
graph.add_node("respond", generate_response)
graph.add_node("decide", decision_logic)
graph.add_node("follow", follow_up_logic)

# Order of execution
graph.set_entry_point("classify")
graph.add_edge("classify", "search")
graph.add_edge("search", "respond")
graph.add_edge("respond", "decide")
graph.add_edge("decide", "follow")

# Compile
workflow = graph.compile()

# ---------------------------------------
# Run the workflow
# ---------------------------------------
final_state = workflow.invoke({"email": email_text})

# ---------------------------------------
# Output
# ---------------------------------------
print("\n------- CLASSIFICATION -------")
print(final_state["classification"])

print("\n------- RESPONSE DRAFT -------")
print(final_state["draft"])

print("\n------- DECISION -------")
print(final_state["decision"])

print("\n------- FOLLOW UP -------")
print(final_state["follow_up"])