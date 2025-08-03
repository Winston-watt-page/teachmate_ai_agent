import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.assessment_agent import generate_assessment
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.subheader("📝 Assessment Builder")
    st.write("Generate MCQs, short/long questions, and case scenarios for your course.")

    with st.form("assessment_form"):
        course_name = st.text_input("Course Title", placeholder="e.g., Data Structures")
        unit_name = st.text_input("Unit / Module", placeholder="e.g., Trees and Graphs")
        num_questions = st.slider("Number of Questions", 5, 20, 10)
        question_type = st.selectbox("Type of Questions", ["MCQs", "Short Answer", "Long Answer", "Case Scenario"])
        bloom_level = st.selectbox("Bloom’s Taxonomy Level", ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"])
        submitted = st.form_submit_button("Generate Questions")

    if submitted:
        if not course_name or not unit_name:
            st.error("Please complete both course and unit/module names.")
            return

        with st.spinner("Generating questions using Gemini..."):
            questions_text = generate_assessment(course_name, unit_name, num_questions, question_type, bloom_level)
            st.success("✅ Assessment Generated!")
            st.markdown("### 🧾 Sample Output")
            st.text(questions_text)

            file_path = export_to_docx(
                title=f"{course_name} – Assessment Bank",
                content=questions_text,
                filename=f"{course_name.replace(' ', '_')}_assessment.docx"
            )
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Assessment (.docx)", f, file_name=os.path.basename(file_path))
