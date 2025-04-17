import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(page_title="Multi-PDF RAG App", layout="wide")

# Initialize session state
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False
    st.session_state.response = ""

# UI
st.title("📄 Multi-PDF Retrieval-Augmented Generation (RAG)")
st.markdown("Upload PDFs and ask questions about their content.")

# PDF Upload
st.subheader("Upload PDFs")
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    files = [('files', (file.name, file.read(), 'application/pdf')) for file in uploaded_files]
    with st.spinner("Processing PDFs..."):
        try:
            response = requests.post(
                'http://localhost:8000/upload',
                files=files
            )
            if response.status_code == 200:
                st.session_state.uploaded = True
                st.success("PDFs processed successfully!")
            else:
                st.error(response.json().get('error', 'Failed to process PDFs'))
        except Exception as e:
            st.error(f"Error uploading PDFs: {str(e)}")

# Query Section
if st.session_state.uploaded:
    st.subheader("Ask a Question")
    query = st.text_input("Enter your question:")
    if st.button("Submit Query"):
        if query:
            with st.spinner("Generating response..."):
                try:
                    response = requests.post(
                        'http://localhost:8000/query',
                        json={'query': query}
                    )
                    if response.status_code == 200:
                        st.session_state.response = response.json()['response']
                        st.markdown("**Answer:**")
                        st.write(st.session_state.response)
                    else:
                        st.error(response.json().get('error', 'Failed to process query'))
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
        else:
            st.warning("Please enter a question.")

# Styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stTextInput>div>input {
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)