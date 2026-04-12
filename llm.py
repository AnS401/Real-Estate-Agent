import requests
from app.config import OPENROUTER_API_KEY, OPENROUTER_URL


def generate_response(context, query, memory):

    prompt = f"""
You are a smart real estate assistant.

Keep responses:
- Short (2–4 lines)
- Natural, not robotic
- Non-repetitive
- Ask 1 follow-up if needed

Context:
{context}

Memory:
{memory}

User:
{query}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        data = res.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("LLM ERROR:", e)

    return None