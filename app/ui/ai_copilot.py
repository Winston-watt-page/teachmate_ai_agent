import streamlit as st
import os
import datetime
from dotenv import load_dotenv

# Import copilot agent
from app.agents.copilot_agent import get_copilot_response

# Load env
load_dotenv()

# Session state for chat memory
if "copilot_history" not in st.session_state:
    st.session_state["copilot_history"] = []

# Streamlit Co-Pilot UI
def render():
    st.subheader("🤖 AI Co-Pilot")
    st.write("Ask your AI assistant anything related to teaching, course planning, or content delivery.")

    user_input = st.text_input("Ask a question...", placeholder="e.g., How to teach recursion visually?")
    
    if st.button("Get Response"):
        if not user_input:
            st.warning("Please type a question.")
            return

        with st.spinner("Thinking..."):
            reply = get_copilot_response(user_input)

            st.session_state["copilot_history"].append({
                "user": user_input,
                "ai": reply,
                "time": datetime.datetime.now().isoformat()
            })

    if st.session_state["copilot_history"]:
        st.markdown("### 🧠 Chat History")
        for chat in reversed(st.session_state["copilot_history"][-10:]):
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**AI Co-Pilot:** {chat['ai']}")
            st.markdown("---")