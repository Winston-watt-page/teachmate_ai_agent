import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.syllabus_agent import generate_syllabus
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.subheader("📘 Syllabus Generator")
    st.write("Enter course details and generate a 15-week structured syllabus.")

    with st.form("syllabus_form"):
        course_name = st.text_input("Course Title", placeholder="e.g., Fundamentals of Data Analytics")
        duration_weeks = st.slider("Course Duration (weeks)", min_value=4, max_value=20, value=15)
        objectives = st.text_area("Learning Objectives", placeholder="What should students achieve by the end of the course?")
        submitted = st.form_submit_button("Generate Syllabus")

    if submitted:
        if not course_name or not objectives:
            st.error("Please fill all required fields.")
            return

        with st.spinner("Generating syllabus using Gemini..."):
            syllabus_text = generate_syllabus(course_name, objectives, duration_weeks)
            st.success("✅ Syllabus Generated!")
            st.markdown(f"### 📖 {course_name} – Weekly Plan")
            st.text(syllabus_text)

            file_path = export_to_docx(
                title=f"{course_name} – Syllabus",
                content=syllabus_text,
                filename=f"{course_name.replace(' ', '_')}_syllabus.docx"
            )
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Syllabus (.docx)", f, file_name=os.path.basename(file_path))
