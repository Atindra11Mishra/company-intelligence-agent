from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_with_groq(prompt: str) -> str:
    """
    Sends prompt to Groq LLM and returns generated text.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior business intelligence analyst. "
                    "Generate source-backed, structured, concise company intelligence reports. "
                    "Do not invent facts. If evidence is weak, clearly say so."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1500
    )

    return response.choices[0].message.content