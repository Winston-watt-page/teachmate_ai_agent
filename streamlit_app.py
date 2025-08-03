import streamlit as st

# Import all tab modules
from app.ui import (
    syllabus_generator,
    lesson_plan_creator,
    assessment_builder,
    resource_recommender,
    feedback_tracker,
    ai_copilot,
    rag_uploader,
    rag_qa
)

# Page configuration
st.set_page_config(
    page_title="TeachMate AI Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔐 Hardcoded user credentials (You can replace with DB later)
USERS = {
    "teacher1": "pass123",
    "admin": "adminpass"
}

# 🔐 Login function
def login():
    st.title("🔐 Login to TeachMate")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                st.success(f"✅ Welcome, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    # else:
    #     st.sidebar.success(f"👋 Logged in as: {st.session_state.username}")
    #     if st.sidebar.button("Logout"):
    #         st.session_state.logged_in = False
    #         st.rerun()

# 🔁 TeachMate Main App UI (only if logged in)
def main_app():
    # Sidebar header
    st.sidebar.title("📘 TeachMate AI Agent")
    st.sidebar.markdown("Empowering educators with AI-powered productivity tools.")
    
    

    # All available tabs
    TABS = {
        "Syllabus Generator": syllabus_generator.render,
        "Lesson Plan Creator": lesson_plan_creator.render,
        "Assessment Builder": assessment_builder.render,
        "Resource Recommender": resource_recommender.render,
        "Feedback Tracker": feedback_tracker.render,
        "Chat with AI Co-Pilot": ai_copilot.render,
        "RAG Document Uploader": rag_uploader.render,
        "RAG-Powered Q&A": rag_qa.render
    }

    # Sidebar navigation
    selected_tab = st.sidebar.radio("🧭 Choose a Module", list(TABS.keys()))
    
     # 🔓 Add logout option
    if st.sidebar.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Header title
    st.title("📚 TeachMate AI Agent – Smart Assistant for Educators")

    # Render selected tab
    TABS[selected_tab]()

# 🚀 Run app
if __name__ == "__main__" or True:
    if "logged_in" in st.session_state and st.session_state.logged_in:
        main_app()
    else:
        login()
