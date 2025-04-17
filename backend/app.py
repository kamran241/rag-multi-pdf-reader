import os
import logging
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from rag import RAGSystem
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app = Flask(__name__)
UPLOAD_FOLDER = 'Uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize RAG system
rag_system = RAGSystem(
    api_key="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",
    model_name='mistralai/mistral-7b-instruct'
)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Multi-PDF RAG API. Use /upload to upload PDFs and /query to ask questions.'}), 200

@app.route('/upload', methods=['POST'])
def upload_pdfs():
    try:
        if 'files' not in request.files:
            logging.error('No files provided in request')
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files')
        file_paths = []

        for file in files:
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
            else:
                logging.warning(f'Invalid file: {file.filename}')
                return jsonify({'error': 'Only PDF files are allowed'}), 400

        rag_system.process_pdfs(file_paths)
        logging.info(f'Processed {len(file_paths)} PDFs')
        return jsonify({'message': 'PDFs processed successfully'}), 200

    except Exception as e:
        logging.error(f'Error processing PDFs: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            logging.error('No query provided')
            return jsonify({'error': 'Query is required'}), 400

        query = data['query']
        response = rag_system.query(query)
        logging.info(f'Query processed: {query}')
        return jsonify({'response': response}), 200

    except Exception as e:
        logging.error(f'Error processing query: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logging.info('Starting Flask server')
    app.run(host='0.0.0.0', port=8000, debug=False)
