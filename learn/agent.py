from langchain.agents import create_agent
from langchain.messages import HumanMessage

system_prompt = """You are a helpful AI assistant. Answer the questions to the best of your ability."""

agent = create_agent(model="gpt-5-nano", system_prompt=system_prompt)

while True:
    userinput = input(f"Ask a question: ")
    question = HumanMessage(content=userinput)
    response = agent.invoke(
        {"messages": [question]}
        )
    print(response['messages'][1].content)