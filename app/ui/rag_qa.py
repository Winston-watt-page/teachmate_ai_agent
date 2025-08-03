import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.rag.rag_retriever import retrieve_similar_context

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def render():
    st.subheader("📖 RAG-Powered Q&A")
    st.write("Ask questions based on uploaded documents.")

    user_query = st.text_input("Ask a question related to your uploaded documents:")

    if st.button("Answer with Context"):
        if not user_query:
            st.warning("Please enter a question.")
            return

        with st.spinner("Retrieving context..."):
            context_chunks = retrieve_similar_context(user_query)

        context = "\n".join(context_chunks)
        prompt = f"""
Use the following context to answer the question:

Context:
{context}

Question:
{user_query}
"""

        response = model.generate_content(prompt)
        st.success("✅ Gemini's Answer:")
        st.text(response.text)