import os
from openai import OpenAI

# The client automatically looks for the OPENAI_API_KEY environment variable
client = OpenAI()

# Example usage (the rest of your code)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "How do I secure my API key?"}]
)
print(response.choices[0].message.content)
