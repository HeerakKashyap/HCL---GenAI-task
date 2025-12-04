from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_system import RAGSystem
from query_processor import QueryProcessor
from embedding_generator import EmbeddingGenerator
from config import Config

app = Flask(__name__)
CORS(app)

rag_system = RAGSystem()
rag_system.initialize(force_rebuild=False)

embedding_generator = EmbeddingGenerator()
query_processor = QueryProcessor(embedding_generator, rag_system.vector_store)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

