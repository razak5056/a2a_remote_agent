
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)


def analyze_data(user_request: str) -> str:
    """Understand a request and analyze the supplied data."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI Data Analysis Agent. "
                    "Analyze the data provided by the user, "
                    "identify patterns and important findings, "
                    "and explain results in simple English. "
                    "Do not invent data that was not provided."
                ),
            },
            {
                "role": "user",
                "content": user_request,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or "No analysis returned."


if __name__ == "__main__":
    request = (
        "Analyze these sales: Product A sold 100 units, "
        "Product B sold 250 units, Product C sold 150 units. "
        "Identify the best-performing product."
    )

    print(analyze_data(request))
