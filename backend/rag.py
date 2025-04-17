import os
import logging
import PyPDF2
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import requests

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/rag.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

class RAGSystem:
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self.dimension = 384  # Embedding dimension for all-MiniLM-L6-v2

    def extract_text_from_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''
                return text
        except Exception as e:
            logging.error(f'Error extracting text from {pdf_path}: {str(e)}')
            raise

    def process_pdfs(self, pdf_paths):
        self.documents = []
        for pdf_path in pdf_paths:
            text = self.extract_text_from_pdf(pdf_path)
            # Split text into chunks (simple split for demo)
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            self.documents.extend(chunks)

        # Create embeddings
        embeddings = self.embedder.encode(self.documents, show_progress_bar=True)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings, dtype='float32'))
        logging.info(f'Processed {len(self.documents)} document chunks')

    def query(self, query_text):
        if not self.index or not self.documents:
            raise ValueError('No documents processed yet')

        # Embed query
        query_embedding = self.embedder.encode([query_text])[0]
        distances, indices = self.index.search(np.array([query_embedding], dtype='float32'), k=3)

        # Retrieve relevant chunks
        context = '\n'.join([self.documents[idx] for idx in indices[0]])

        # Call OpenRouter API
        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model_name,
                    'messages': [
                        {'role': 'system', 'content': 'You are a helpful assistant. Answer based on the provided context.'},
                        {'role': 'user', 'content': f'Context: {context}\n\nQuery: {query_text}'}
                    ]
                }
            )
            response.raise_for_status()
            answer = response.json()['choices'][0]['message']['content']
            return answer
        except Exception as e:
            logging.error(f'Error calling OpenRouter API: {str(e)}')
            raise