import os
import fitz  # PyMuPDF for PDFs
import docx
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Load embedding model
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("teachmate_rag")

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

# Extract text from TXT
def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Read any supported document
def read_document(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format.")

# Split text into overlapping chunks
def chunk_text(text, max_words=120, overlap=20):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + max_words]
        chunks.append(" ".join(chunk))
        i += max_words - overlap
    return chunks

# Upload and embed document to ChromaDB
def upload_and_embed_document(file_path, source_label):
    raw_text = read_document(file_path)
    chunks = chunk_text(raw_text)

    embeddings = sentence_model.encode(chunks).tolist()
    ids = [f"{source_label}_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": source_label}] * len(chunks)
    )

    return len(chunks)

# Retrieve relevant chunks based on a query
def retrieve_similar_context(query, top_k=5):
    query_embedding = sentence_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    return documents if documents else []