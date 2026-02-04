from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from IPython.display import display, Markdown


llm = ChatOpenAI(model="gpt-5-nano")

system_template = """You are a travel planning assistant. 
Your task is to help users plan their trips by providing recommendations on destinations, 
accommodations, activities, and dining options based on their preferences and budget. Remove any formatting from your response."""


travel_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", """I am planning a trip to {destination} for {duration} days.
                My budget is {budget} USD.
                I enjoy {interests}. Can you suggest an itinerary for me?""")
])


parser = StrOutputParser()

travel_agent_chain = travel_agent_prompt | llm | parser

def plan_trip(destination: str, duration: int, budget: int, interests: str) -> str:
    response = travel_agent_chain.invoke({
        "destination": destination,
        "duration": duration,
        "budget": budget,
        "interests": interests
    })
    return response


#def render_itinerary(itinerary: str):
#    display(Markdown(itinerary))

# Example usage
result = plan_trip(
    destination="Paris",
    duration=7,
    budget=2000,
    interests="culture, food, nature"
)

#render_itinerary(result)

print(result)
