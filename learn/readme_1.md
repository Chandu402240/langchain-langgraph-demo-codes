**Prompt Quality Scoring Agent – Assignment**

**Assignment:** Build a Prompt Quality Scoring Agent Using LangChain

**Objective:**
Build a simple LangChain agent that takes a prompt as input, evaluates its quality, assigns a score out of 10, and provides feedback and improvement suggestions.
What the Agent Should Do:
Input: A single text prompt

**Output:**
- Final score (0–10)
- Scores for each quality criterion
- Short explanation
- 2–3 suggestions to improve the prompt

**Prompt Quality Criteria:**
1. Clarity (0–10): Checks whether the prompt is easy to understand and has a clear goal.
2. Specificity / Details (0–10): Evaluates whether sufficient details and requirements are provided.
3. Context (0–10): Checks if background information, audience, or use case is mentioned.
4. Output Format & Constraints (0–10): Checks whether expected output format, tone, or length is specified.
5. Persona defined (0–10): Confirms whether a prompt assigns a specific role.

**Final Score Calculation:**
The final score should be the average of the five criteria.


**Solution:**
prompt_quality.py is the code for this assignment.
Execute the code using > python3 prompt_quality.py

**Examples:**
Provide a prompt to evaluate: You are a programmer, provide me a python program to create a small website and program should be less that 50 lines of code.
{
  "final_score": 4.8,
  "criteria": [
    {"criterion": "Clarity", "score": 7},
    {"criterion": "Specificity / Details", "score": 3},
    {"criterion": "Context", "score": 3},
    {"criterion": "Output Format & Constraints", "score": 5},
    {"criterion": "Persona defined", "score": 6}
  ],
  "explain": "Clear goal, but lacks feature details, context, and output specifics.",
  "improvements": [
    "Specify framework, Python version, and required routes/features.",
    "Define environment, dependencies, and how to run locally.",
    "Set output format: single-file code block, under 50 lines."
  ]
}
Provide a prompt to evaluate: You need to validate Json, provide input for json and will validation.
{
  "final_score": 0.6,
  "criteria": [
    {"criterion": "Clarity", "score": 2},
    {"criterion": "Specificity / Details", "score": 1},
    {"criterion": "Context", "score": 0},
    {"criterion": "Output Format & Constraints", "score": 0},
    {"criterion": "Persona defined", "score": 0}
  ],
  "explain": "Unclear phrasing; missing specifics, context, output constraints, and persona.",
  "improvements": [
    "State the exact JSON schema and required fields.",
    "Describe input examples and expected validation error messages.",
    "Define the validator's role, tone, and output format."
  ]
}
Provide a prompt to evaluate: """ You are a travel agent and you can only suggest 3 day itinerary for enquiry from user. Also you can suggest only itinerary for New Jersey, USA state.You need to provide output like # Day 1 : plan in 10 words, Day 2 : plan in 10 words and Day 3 : Plan in 10 words.If you are asked for some other state, please clearly provide information that you cannot provide as you are not trained for that data points."""
{
  "final_score": 6.6,
  "criteria": [
    {"criterion": "Clarity", "score": 7},
    {"criterion": "Specificity / Details", "score": 6},
    {"criterion": "Context", "score": 6},
    {"criterion": "Output Format & Constraints", "score": 6},
    {"criterion": "Persona defined", "score": 8}
  ],
  "explain": "Clear persona and scope, but formatting, word-count rules, and user context lack specificity.",
  "improvements": [
    "Define exact output lines and separators for each day.",
    "Clarify whether punctuation counts toward the ten-word limit.",
    "Include user preferences: season, budget, interests, travel pace."
  ]
}