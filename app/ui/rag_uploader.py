import streamlit as st
import os
import shutil
from app.rag.rag_retriever import upload_and_embed_document

# Define upload directory
UPLOAD_DIR = "docs/sample_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Streamlit UI
def render():
    st.subheader("📂 RAG Document Uploader")
    st.write("Upload course materials (PDF, DOCX, TXT) to embed for question-answering.")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

    if uploaded_file:
        filename = uploaded_file.name
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Uploaded: {filename}")

        # Embed and store in ChromaDB
        with st.spinner("Embedding document into vector DB..."):
            try:
                num_chunks = upload_and_embed_document(file_path, source_label=filename)
                st.success(f"✅ Document embedded successfully! {num_chunks} chunks stored.")
            except Exception as e:
                st.error(f"❌ Failed to embed: {str(e)}")

        # Show file path
        st.info(f"Stored in: `{file_path}`")