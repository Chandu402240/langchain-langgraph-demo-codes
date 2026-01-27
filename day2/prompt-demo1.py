from langchain_ollama import ChatOllama

llm = ChatOllama(model = "gemma2:2b")

user_prompt = "you are a helpful assistant. What is my NAME ?"

response = llm.invoke(user_prompt)

print(response.text)