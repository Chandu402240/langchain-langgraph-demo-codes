# ---------------------------------------------------------
# SIMPLE AI CUSTOMER SUPPORT WORKFLOW
# Using: openai, langchain, langgraph
# No classes, no complex structure
# ---------------------------------------------------------

from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

client = OpenAI()

# ---------------------------------------------------------
# Input Email (You can change this to test)
# ---------------------------------------------------------

email_text = """
Hi team, I was charged twice for my subscription yesterday.
Please fix this immediately!
"""

# ---------------------------------------------------------
# STEP 1 — Classify Urgency
# ---------------------------------------------------------

prompt_urgency = ChatPromptTemplate.from_messages([
    ("system", "Classify email urgency as Low, Medium, or High."),
    ("user", "{email}")
])

chain_urgency = prompt_urgency | client.chat.completions.create | StrOutputParser()
urgency = chain_urgency.invoke({"email": email_text})


# ---------------------------------------------------------
# STEP 2 — Classify Topic
# ---------------------------------------------------------

prompt_topic = ChatPromptTemplate.from_messages([
    ("system", "Classify topic into: Account, Billing, Bug, Feature Request, Technical Issue."),
    ("user", "{email}")
])

chain_topic = prompt_topic | client.chat.completions.create | StrOutputParser()
topic = chain_topic.invoke({"email": email_text})


# ---------------------------------------------------------
# STEP 3 — Search Knowledge Base (using LLM instead of real search)
# ---------------------------------------------------------

prompt_kb = ChatPromptTemplate.from_messages([
    ("system", "Pretend you are searching company documentation. Return helpful information."),
    ("user", "{email}")
])

chain_kb = prompt_kb | client.chat.completions.create | StrOutputParser()
kb_notes = chain_kb.invoke({"email": email_text})


# ---------------------------------------------------------
# STEP 4 — Draft a Response
# ---------------------------------------------------------

prompt_answer = ChatPromptTemplate.from_messages([
    ("system", "Write a clear and polite support email reply using the notes and classifications."),
    ("user", "Email: {email}\nUrgency: {urgency}\nTopic: {topic}\nKB Info: {kb}")
])

chain_answer = prompt_answer | client.chat.completions.create | StrOutputParser()
draft_reply = chain_answer.invoke({
    "email": email_text,
    "urgency": urgency,
    "topic": topic,
    "kb": kb_notes
})


# ---------------------------------------------------------
# STEP 5 — Decide Escalation
# ---------------------------------------------------------

prompt_escalation = ChatPromptTemplate.from_messages([
    ("system", "Decide: auto-reply (Yes/No) and escalation (None/Human). Be strict."),
    ("user", "{email}\nUrgency: {urgency}\nTopic: {topic}")
])

chain_escalation = prompt_escalation | client.chat.completions.create | StrOutputParser()
escalation = chain_escalation.invoke({
    "email": email_text,
    "urgency": urgency,
    "topic": topic
})


# ---------------------------------------------------------
# STEP 6 — Follow-up Recommendation
# ---------------------------------------------------------

prompt_followup = ChatPromptTemplate.from_messages([
    ("system", "Does this email require a follow-up action? Reply Yes or No, and reason."),
    ("user", "{email}")
])

chain_followup = prompt_followup | client.chat.completions.create | StrOutputParser()
followup = chain_followup.invoke({"email": email_text})


# ---------------------------------------------------------
# OUTPUT RESULTS
# ---------------------------------------------------------

print("\n============================")
print("  AI SUPPORT AGENT OUTPUT")
print("============================\n")

print("EMAIL INPUT:\n", email_text)
print("\nURGENCY:", urgency)
print("TOPIC:", topic)
print("\nKB SEARCH RESULT:\n", kb_notes)
print("\nDRAFT RESPONSE:\n", draft_reply)
print("\nESCALATION DECISION:\n", escalation)
print("\nFOLLOW-UP ACTION:\n", followup)
