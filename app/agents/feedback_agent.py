import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Load API key from .env and configure
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_feedback_suggestions(course_name: str, what_worked: str, what_did_not: str) -> str:
    # Input validation
    if not course_name.strip() or not what_worked.strip() or not what_did_not.strip():
        return "⚠️ Please provide course name, what worked, and what didn’t work to generate suggestions."

    # Enhanced Prompt
    prompt = f"""
🎓 You are an AI academic mentor reviewing weekly feedback for a course titled **"{course_name}"**.

✅ Positive aspects that worked well:
{what_worked}

❌ Areas that did not work effectively:
{what_did_not}

📌 Based on the feedback, suggest **2–3 specific, practical, and constructive improvements** to enhance future teaching sessions.

🧠 Suggestions should:
- Be realistic and actionable
- Maintain a supportive tone
- Align with good teaching practices
- Help the educator improve without sounding critical

Format your response using clear bullet points.
"""

    # Error-safe generation
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Failed to generate feedback suggestions: {str(e)}"
