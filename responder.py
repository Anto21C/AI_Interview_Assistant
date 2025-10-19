import os
import requests
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "gpt-oss-20b"

# Optional intros to make answers more human-like
HUMAN_INTROS = [
    "In my experience, ",
    "Typically, ",
    "I would say that ",
    "From my perspective, ",
    "Generally speaking, ",
    "I believe that ",
]

def get_ai_response(prompt):
    if not API_KEY:
        return "⚠️ Missing OpenRouter API key. Add it to your .env file."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    system_message = {
        "role": "system",
        "content": (
            "You are a highly professional and friendly AI interview assistant. "
            "Answer questions naturally, like a human would in a real interview. "
            "Use clear, concise sentences and provide reasoning or examples when appropriate. "
            "Maintain a polite and confident tone. "
            "Use expressions like 'I would', 'In my experience', 'Typically', and avoid sounding robotic. "
            "Structure answers so they are easy to follow and conversational. "
            "Keep answers engaging, human-like, and relevant to the question."
        )
    }

    payload = {
        "model": MODEL,
        "messages": [
            system_message,
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85,  # human-like variation
        "max_tokens": 600,    # detailed, complete answers
        "top_p": 0.9
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            message = data["choices"][0].get("message", {})
            content = message.get("content", "").strip()
            if content:
                # Prepend a random human-like intro for natural flow
                intro = random.choice(HUMAN_INTROS)
                humanized_content = intro + content[0].lower() + content[1:]
                return humanized_content
        return "⚠️ No content received from GPT-OSS-20B."
    except requests.exceptions.RequestException as e:
        return f"🌐 Network error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
