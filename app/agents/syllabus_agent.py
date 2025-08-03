import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Load environment and configure Gemini
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_syllabus(course_name: str, objectives: str, duration_weeks: int = 15) -> str:
    # Input validation
    if not course_name.strip() or not objectives.strip():
        return "⚠️ Course name and objectives cannot be empty."

    # Improved Prompt
    prompt = f"""
📘 You are an AI-powered academic syllabus designer.

🎯 Goal: Create a week-by-week syllabus plan for a university-level course titled: "{course_name}"
📆 Duration: {duration_weeks} weeks
📌 Course Objectives:
{objectives}

🔖 Output Format:
- Each week should include:
  • 📚 Main topic(s)
  • 🔍 Suggested subtopics
  • 🎯 Weekly activity (e.g., quiz, lab, group discussion, case study)

📝 Use clean bullet points, numbered by week.
💡 Be concise, aligned to undergraduate curriculum.
🚫 Do not include assessment rubrics or grading — focus only on syllabus flow.
"""

    # Error handling
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Failed to generate syllabus: {str(e)}"