import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_assessment(course_name: str, unit_name: str, num_questions: int, question_type: str, bloom_level: str) -> str:
    # ✅ Improved Prompt
    prompt = f"""
You are an expert academic content creator.

Generate exactly {num_questions} {question_type.upper()} questions for the following details:

📘 Course: {course_name}
📕 Unit: {unit_name}

🧠 Cognitive Level: {bloom_level.title()} – as per Bloom's Taxonomy. Ensure all questions meet this level.
💡 Format: Use a clean numbered list (e.g., 1., 2., …)
🔄 Variety: Include a mix of difficulty levels and concepts within the unit.
🎯 Curriculum: Align with standard undergraduate course outcomes.

Note:
- For MCQs, give 4 options (A–D) and mark the correct answer with **(Answer: )**
- Avoid repetition and ensure clarity.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # ⚠️ Error Handling: catches and reports AI-related issues
        return f"❌ Error generating assessment: {str(e)}"
