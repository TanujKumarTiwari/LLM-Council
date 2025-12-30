from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # dummy key, required by client
)

def generate_answer(question: str, temperature=0.7) -> str:
    response = client.chat.completions.create(
        model="llama3.2:latest",
        messages=[{"role": "user", "content": question}],
        temperature=temperature
    )
    return response.choices[0].message.content
def generate_detailed_answer(question: str, temperature=0.7) -> str:
    prompt = f"Provide a detailed and comprehensive answer to the following question:\n\n{question}\n\nInclude explanations, examples, and relevant context."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content