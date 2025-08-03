import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel

import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_lesson_plan(course_name: str, duration: str, difficulty: str, outcomes: str, num_weeks: int = 12) -> str:
    prompt = f"""Create a weekly lesson plan for a course titled "{course_name}" lasting {num_weeks} weeks.
Class duration per week: {duration}
Student level: {difficulty}
Target learning outcomes:
{outcomes}

Format output in bullet points with topic, subtopics, and suggested activities for each week."""
    response = model.generate_content(prompt)
    return response.text
