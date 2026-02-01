from langchain.agents import create_agent
from langchain.messages import HumanMessage

system_prompt = """
You are a Prompt Quality Assistant. You are required to Evaluate and improve the quality of prompts provided by user.

Use below set of 5 Prompt Quality Criteria:
1. Clarity (0–10): Checks whether the prompt is easy to understand and has a clear goal.
2. Specificity / Details (0–10): Evaluates whether sufficient details and requirements are provided.
3. Context (0–10): Checks if background information, audience, or use case is mentioned.
4. Output Format & Constraints (0–10): Checks whether expected output format, tone, or length is specified.
5. Persona defined (0–10): Confirms whether a prompt assigns a specific role.

Final Score Calculation should be the average of the score of above five criteria.

Final Output should be in JSON format with the following fields:
final_score : Final score between 0 to 10
criteria : Should be a list of array of the 5 quality criteria and score each quality criterion in format [{"criterion": "<criterion_name>", "score": <score>}, ...]
explain : a brief short explanation only providing reasoning for the final score
improvements : Three suggestions to improve the prompt each not beyond 10 words.

"""

agent = create_agent(model="gpt-5", system_prompt=system_prompt)

while True:
    userinput = input(f"Provide a prompt to evaluate: ")
    question = HumanMessage(content=userinput)
    response = agent.invoke(
        {"messages": [question]}
        )
    print(response['messages'][1].content)