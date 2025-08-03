import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Load API key from .env and configure
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_resources(topic: str, difficulty: str, format_types: list) -> str:
    # Input validation
    if not topic.strip() or not difficulty.strip() or not format_types:
        return "⚠️ Error: Topic, difficulty, and at least one format type are required."

    # Format types into a clean comma-separated string
    formats = ', '.join(format_types)

    # Enhanced Prompt
    prompt = f"""
🎓 You are an AI-powered education assistant specialized in academic content curation.

📌 Task: Recommend **high-quality, open-access online resources** to help educators teach the topic: **"{topic}"**  
🎯 Student level: {difficulty}

🔖 Preferred content formats: {formats}

💡 Guidelines:
- Include a mix of formats such as blogs, PDFs, video lectures, tutorials, research papers, or case studies.
- Prioritize well-known, credible sources (e.g., Khan Academy, MIT OCW, Coursera, arXiv).
- Add **titles** with **links** (if available).
- List in **clean bullet points**, grouped by format if possible.
- Avoid paywalled content or overly promotional material.

Your response should be concise, educator-friendly, and easy to scan.
"""

    # Error-safe generation
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Failed to generate resources: {str(e)}"
