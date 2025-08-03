import streamlit as st
import os
import datetime
import json
from dotenv import load_dotenv
from app.agents.feedback_agent import generate_feedback_suggestions
from app.utils.file_exporter import export_to_docx

load_dotenv()
feedback_log_path = "app/memory/feedback_log.json"

def save_feedback(course_name, positive, negative, suggestions):
    entry = {
        "course": course_name,
        "timestamp": datetime.datetime.now().isoformat(),
        "what_worked": positive,
        "what_did_not": negative,
        "gemini_suggestion": suggestions
    }

    if os.path.exists(feedback_log_path):
        with open(feedback_log_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(feedback_log_path, "w") as f:
        json.dump(data, f, indent=2)

def render():
    st.subheader("📊 Feedback Tracker")
    st.write("Log your weekly reflection and get smart suggestions from AI.")

    with st.form("feedback_form"):
        course_name = st.text_input("Course Name", placeholder="e.g., Machine Learning")
        positive = st.text_area("✅ What went well?")
        negative = st.text_area("❌ What needs improvement?")
        submitted = st.form_submit_button("Generate Suggestions")

    if submitted:
        if not course_name or not positive or not negative:
            st.error("All fields are required.")
            return

        with st.spinner("Analyzing your feedback with Gemini..."):
            suggestions = generate_feedback_suggestions(course_name, positive, negative)
            st.success("✅ Suggestions Ready!")
            st.markdown("### 💡 Gemini Suggestions")
            st.text(suggestions)

            save_feedback(course_name, positive, negative, suggestions)

            file_path = export_to_docx(
                title=f"{course_name} – Weekly Feedback Summary",
                content=suggestions,
                filename=f"{course_name.replace(' ', '_')}_feedback_summary.docx"
            )
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Feedback Summary (.docx)", f, file_name=os.path.basename(file_path))
