from langchain_ollama import ChatOllama

llm = ChatOllama(model="functiongemma")

response = llm.invoke("what is 2+2?")

print(response.content)

# Expected output: "2+2 is 4."
