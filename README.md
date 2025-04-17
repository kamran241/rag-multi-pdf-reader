Multi-PDF RAG Application
A professional Retrieval-Augmented Generation (RAG) application for processing multiple PDFs and answering queries using a Flask backend and Streamlit frontend.
Prerequisites

Python 3.13.3
pip
Virtual environment (recommended)

Setup
    ```bash
    Clone the repository:
    git clone https://github.com/kamran241/rag-multi-pdf-reader.git
    cd rag-multi-pdf-reader.git


Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Set up environment variables:

Create a .env file in the root directory.

Add your OpenRouter API key:
OPENROUTER_API_KEY=your-api-key




Create necessary directories:
mkdir -p backend/logs uploads



Running the Application

Start the Flask backend:
    ```bash 
       cd backend
       python app.py

The backend runs on http://localhost:8000.

Start the Streamlit frontend: Open a new terminal, activate the virtual environment, and run:
        ```bash
           cd frontend
           streamlit run app.py

The frontend runs on http://localhost:8501.


Usage

Open the Streamlit UI in your browser (http://localhost:8501).
Upload one or more PDF files.
Enter a question about the PDF content and submit to get a response.

Troubleshooting

Ensure the Flask backend is running before starting the Streamlit frontend.
Check backend/logs/app.log and backend/logs/rag.log for errors.
Verify the OpenRouter API key is correct in .env.

Notes

The app uses the deepseek-chat-v3-0324 model via OpenRouter.
PDFs are processed locally, and text is split into 500-character chunks for RAG.
The vector store uses FAISS with all-MiniLM-L6-v2 embeddings.

