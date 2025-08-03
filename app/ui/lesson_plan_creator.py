import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.lesson_plan_agent import generate_lesson_plan
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.subheader("🧾 Lesson Plan Creator")
    st.write("Generate a detailed weekly lesson plan with class time, level, and outcomes.")

    with st.form("lesson_plan_form"):
        course_name = st.text_input("Course Title", placeholder="e.g., Fundamentals of AI")
        num_weeks = st.slider("Number of Weeks", 4, 20, 12)
        class_duration = st.selectbox("Class Duration per Week", ["1 hour", "2 hours", "3 hours"])
        target_outcomes = st.text_area("Target Learning Outcomes")
        difficulty = st.selectbox("Student Level", ["Beginner", "Intermediate", "Advanced"])
        submitted = st.form_submit_button("Generate Lesson Plan")

    if submitted:
        if not course_name or not target_outcomes:
            st.error("All fields are required.")
            return

        with st.spinner("Generating weekly lesson plan..."):
            lesson_text = generate_lesson_plan(course_name, class_duration, difficulty, target_outcomes, num_weeks)
            st.success("✅ Lesson Plan Ready!")
            st.markdown("### 📅 Weekly Lesson Breakdown")
            st.text(lesson_text)

            file_path = export_to_docx(
                title=f"{course_name} – Lesson Plan",
                content=lesson_text,
                filename=f"{course_name.replace(' ', '_')}_lesson_plan.docx"
            )
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Lesson Plan (.docx)", f, file_name=os.path.basename(file_path))
