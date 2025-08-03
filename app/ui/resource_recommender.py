import streamlit as st
import os
from dotenv import load_dotenv
from app.agents.resource_agent import generate_resources
from app.utils.file_exporter import export_to_docx

load_dotenv()

def render():
    st.subheader("🔍 Resource Recommender")
    st.write("Get curated academic resources based on topic and learning level.")

    with st.form("resource_form"):
        subject = st.text_input("Topic / Concept", placeholder="e.g., Natural Language Processing")
        difficulty = st.selectbox("Student Level", ["Beginner", "Intermediate", "Advanced"])
        format_types = st.multiselect(
            "Preferred Resource Types",
            ["YouTube Videos", "Blogs", "Slides (PPT)", "PDFs", "Research Papers", "Lab Assignments", "Case Studies"],
            default=["YouTube Videos", "PDFs"]
        )
        submitted = st.form_submit_button("Generate Resources")

    if submitted:
        if not subject or not format_types:
            st.error("Please fill the topic and choose at least one format.")
            return

        with st.spinner("Generating suggestions using Gemini..."):
            resources_text = generate_resources(subject, difficulty, format_types)
            st.success("✅ Resources Generated!")
            st.markdown("### 📚 Suggested Resources")
            st.text(resources_text)

            file_path = export_to_docx(
                title=f"{subject} – Suggested Resources",
                content=resources_text,
                filename=f"{subject.replace(' ', '_')}_resources.docx"
            )
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Resources (.docx)", f, file_name=os.path.basename(file_path))
