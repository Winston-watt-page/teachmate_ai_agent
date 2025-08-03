import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel

import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_copilot_response(query: str) -> str:
    if not query.strip():
        return "⚠️ Please enter a valid teaching-related query."

    prompt = f"""
🎓 You are an expert AI Teaching Co-Pilot designed to support educators.

✅ Your goals:
- Provide clear, actionable answers
- Suggest engaging classroom activities
- Support lesson planning and teaching strategies
- Explain complex concepts in simple language

📩 Educator's Query:
{query}

📘 Respond with empathy, clarity, and professional tone. Use bullet points or formatting if needed.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error fetching copilot response: {str(e)}"
