from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from rag_system import RAGSystem
from query_processor import QueryProcessor
from embedding_generator import EmbeddingGenerator
from document_processor import DocumentProcessor
from chunking_strategies import ChunkingStrategies
from config import Config

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = Config.DOCUMENTS_PATH
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

rag_system = RAGSystem()
rag_system.initialize(force_rebuild=False)

embedding_generator = EmbeddingGenerator()
query_processor = QueryProcessor(embedding_generator, rag_system.vector_store)
document_processor = DocumentProcessor()
chunking_strategies = ChunkingStrategies()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'OK',
        'initialized': rag_system.initialized,
        'stats': rag_system.get_stats()
    })

@app.route('/api/query', methods=['POST'])
def query():
    if not rag_system.initialized:
        return jsonify({'error': 'RAG system not initialized'}), 500
    
    try:
        data = request.json
        user_query = data.get('query', '')
        use_transformation = data.get('use_transformation', True)
        
        if not user_query:
            return jsonify({'error': 'Query is required'}), 400
        
        result = query_processor.process_query(user_query, use_transformation)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rebuild', methods=['POST'])
def rebuild():
    try:
        rag_system.initialize(force_rebuild=True)
        return jsonify({
            'message': 'Vector store rebuilt successfully',
            'stats': rag_system.get_stats()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify(rag_system.get_stats())

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            if filename.endswith('.pdf'):
                text = document_processor.extract_text_from_pdf(filepath)
            elif filename.endswith('.txt'):
                text = document_processor.extract_text_from_txt(filepath)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
            
            if not text or len(text.strip()) < 50:
                os.remove(filepath)
                return jsonify({'error': 'File is empty or too short'}), 400
            
            cleaned_text = document_processor.clean_text(text)
            
            doc = {
                'filename': filename,
                'content': cleaned_text,
                'source': filepath
            }
            
            metadata = {
                'filename': filename,
                'source': filepath
            }
            
            chunks = chunking_strategies.apply_all_techniques([doc])
            
            chunks_with_embeddings = embedding_generator.generate_chunk_embeddings(chunks)
            
            rag_system.vector_store.add_chunks(chunks_with_embeddings)
            rag_system.vector_store.save()
            
            return jsonify({
                'message': f'File {filename} uploaded and processed successfully',
                'filename': filename,
                'chunks_created': len(chunks),
                'stats': rag_system.get_stats()
            })
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Only PDF and TXT files are allowed'}), 400

@app.route('/api/documents', methods=['GET'])
def list_documents():
    documents = []
    if os.path.exists(Config.DOCUMENTS_PATH):
        for filename in os.listdir(Config.DOCUMENTS_PATH):
            if filename.endswith(('.pdf', '.txt')):
                filepath = os.path.join(Config.DOCUMENTS_PATH, filename)
                size = os.path.getsize(filepath)
                documents.append({
                    'filename': filename,
                    'size': size,
                    'type': 'pdf' if filename.endswith('.pdf') else 'txt'
                })
    return jsonify({'documents': documents})

@app.route('/api/documents/<filename>', methods=['DELETE'])
def delete_document(filename):
    try:
        filepath = os.path.join(Config.DOCUMENTS_PATH, secure_filename(filename))
        if os.path.exists(filepath):
            os.remove(filepath)
            rag_system.initialize(force_rebuild=True)
            return jsonify({
                'message': f'Document {filename} deleted successfully',
                'stats': rag_system.get_stats()
            })
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

