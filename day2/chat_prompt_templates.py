from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="gemma2:2b")

prompt_template = ChatPromptTemplate.from_messages([
("system", "You are a helpful assistant and your task is to summarize the given topic in 20 words with no markdown formatting in response"),
("human", "Write a summary about {topic}")
])


while True:
    topic = input("What topic do you want me to summarize")
    print(f"{prompt_template.format(topic=topic)}")
    response = llm.invoke(prompt_template.format(topic = topic))
    print(f"Assistant: {response.text}")
