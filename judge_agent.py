import json
import re
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # dummy key, required by client
)

RUBRIC = """
Score each answer from 0–10 for:
- Correctness
- Completeness
- Clarity
- Safety

Return ONLY a JSON object with no other text:
{ "score": number }
"""

def judge(question: str, answer: str) -> float:
    response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": RUBRIC},
            {"role": "user", "content": f"Q: {question}\nA: {answer}"}
        ],
        temperature=0
    )
    
    content = response.choices[0].message.content
    
    # Try to extract JSON from the response
    try:
        # First try direct JSON parsing
        data = json.loads(content)
        return float(data["score"])
    except:
        # Try to find JSON object in the text
        match = re.search(r'\{[^}]*"score"\s*:\s*(\d+\.?\d*)[^}]*\}', content)
        if match:
            return float(match.group(1))
        # If all else fails, return a default score
        print(f"Warning: Could not parse score from: {content}")
        return 5.0  # Default middle score
