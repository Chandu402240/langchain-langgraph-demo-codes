from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOllama(model="gemma2:2b")

system_message = """
You are a travel assistant
Rules:
- Answer only travel-related questions
- If the question is not travel-related, reply:
"I can help only with travel related questions."

Response format:
- Always start the response with username. for example -  "Hi {username}, Here is the answer to you question."
- Short direct answer
- Bullet points if needed
- Do NOT use *, -, **, or Markdown
- address user with username

User question: {question}"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template("{question}")
])
username = input("Hey there, May I know your name please: ")



while True:
    question = input("Enter your question")
    response = llm.invoke(template.format(
                    username = username, 
                    question = question
                ))
    print(f"Assistant : {response.text}")