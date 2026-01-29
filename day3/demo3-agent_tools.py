from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
from langchain_tavily import TavilySearch
from tavily import TavilyClient
# ============================== TAVILY SEARCH API  =================================


llm = ChatOllama(model = "qwen3:0.6b")

@tool
def web_search_with_tavily(query: str):

    """
    This is a tool to help you with the web search
    """
    client = TavilyClient("Put in your private Tavily Api Key")
    response = client.search(
    query=query,
    search_depth="advanced")
    return response


system_prompt = """
You are a helpful assistant Agent.

You have been given access to get_username, get_weather tool, web_search_with_tavily to search the info on the internet

Use the available tool as required by the User.

Use Reason, Think, Act approach

"""


prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

@tool
def get_username():
    """
    To get the username, we can use this tool
    """
    return "Shubham"
@tool
def get_weather(city: str):
    """
    To get the weather of the current city or location
    """
    return "Weather in {city} is sunny today"

tools = [get_username, get_weather, web_search_with_tavily]

llm_with_tools = llm.bind_tools(tools)


agent = create_tool_calling_agent(llm = llm_with_tools, tools = tools, prompt = prompt_template)

agent_executor = AgentExecutor(agent=agent, tools = tools, verbose = True)


while True:
    user_prompt = input("Please enter your question \n")
    result = agent_executor.invoke({"input":user_prompt})
    print(result)


