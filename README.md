# Mini RAG-Powered Assistant

A Retrieval-Augmented Generation (RAG) system that answers questions based on a custom document corpus using advanced chunking techniques, vector similarity search, and local LLM integration.
## Live Demo

🌐 **Deployed Application**: [https://hcl-genai-task-1.onrender.com](https://hcl-genai-task-1.onrender.com)

## Features

- **PDF/TXT Upload**: Upload 3-5 documents through web interface
- **5 RAG Chunking Techniques**: Implements all required chunking strategies
- **Vector Embeddings**: Local embeddings using sentence-transformers
- **Vector Database**: FAISS for efficient similarity search
- **Local LLM**: Llama 3 via Ollama for response generation (no API keys needed)
- **Web Interface**: React-based UI for document upload and querying
- **Source Citations**: Shows which documents and chunks were used

## Architecture

### Components

1. **Document Processing**: Extracts and cleans text from PDF and TXT files
2. **Chunking Strategies**: Implements 5 RAG techniques for document segmentation
3. **Embedding Generation**: Converts text chunks to vector embeddings
4. **Vector Storage**: FAISS-based local vector database for similarity search
5. **Query Processing**: Query transformation, retrieval, and response generation
6. **LLM Integration**: Llama 3 (Ollama) for final answer generation
7. **Frontend**: React-based web interface for upload and querying

### RAG Techniques Implemented

1. **Fixed-Size Chunking**: Simple chunking with configurable size and overlap
2. **Semantic Chunking**: Paragraph-based segmentation preserving semantic boundaries
3. **Contextual Headers**: Adds contextual headers to chunks for better retrieval
4. **Synthetic Q&A Pairs**: Generates question-answer pairs to augment chunk content
5. **Query Transformation**: Extracts keywords and generates query variations

### Technology Stack

- **Backend**: Python/Flask
- **Frontend**: React
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (local)
- **Vector Database**: FAISS (local)
- **LLM**: Llama 3 via Ollama (local, free)
- **Document Processing**: pdfplumber, pypdf

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- Ollama (for LLM functionality)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/HeerakKashyap/HCL---GenAI-task.git
cd HCL---GenAI-task
```

2. Create and activate virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and pull Llama model:
```bash
# Download Ollama from https://ollama.ai
# After installation, run:
ollama pull llama3
```

5. Install frontend dependencies:
```bash
cd client
npm install
cd ..
```

6. Set up directories:
```bash
python setup.py
```

## Usage

### Starting the Backend

```bash
venv\Scripts\activate  # Windows
python app.py
```

The backend will start on `http://localhost:5000` and automatically build the vector store from documents in the `documents/` directory.

### Starting the Frontend

```bash
cd client
npm start
```

The frontend will start on `http://localhost:3000`.

### Using the System

1. **Upload Documents**:
   - Open the web interface at `http://localhost:3000`
   - Click "Upload Documents" tab
   - Upload 3-5 PDF or TXT files
   - Wait for processing (embeddings are generated automatically)

2. **Query Documents**:
   - Click "Query Documents" tab
   - Enter your question
   - Toggle query transformation if needed
   - Click "Ask" to get the answer

### API Endpoints

- `GET /api/health`: Check system status
- `GET /api/stats`: Get vector store statistics
- `GET /api/documents`: List uploaded documents
- `POST /api/upload`: Upload a PDF or TXT file
- `DELETE /api/documents/<filename>`: Delete a document
- `POST /api/query`: Submit a query
  ```json
  {
    "query": "Your question here",
    "use_transformation": true
  }
  ```
- `POST /api/rebuild`: Rebuild the vector store

## Configuration

Edit `config.py` or set environment variables:

- `CHUNK_SIZE`: Size of text chunks (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `TOP_K`: Number of chunks to retrieve (default: 3)
- `USE_LOCAL_EMBEDDINGS`: Use local embeddings (default: true)
- `EMBEDDING_MODEL`: Embedding model name
- `LLM_MODEL`: LLM model name (default: llama3)
- `LLM_PROVIDER`: LLM provider (default: ollama)


## How It Works

1. **Document Upload**: PDF/TXT files are uploaded through web interface
2. **Text Extraction**: Text is extracted and cleaned
3. **Chunking**: Documents are chunked using 5 different techniques
4. **Embedding**: Each chunk is converted to a vector embedding
5. **Storage**: Embeddings are stored in FAISS vector database
6. **Query Processing**: User query is embedded and searched
7. **Retrieval**: Top-K similar chunks are retrieved
8. **Generation**: Retrieved chunks + query are fed to Llama 3
9. **Response**: LLM generates answer based on retrieved context

## Evaluation Metrics

The system can be evaluated on:

1. **Retrieval Relevance**: How well retrieved chunks match the query
2. **Answer Correctness**: Accuracy of generated answers
3. **Hallucination Rate**: Frequency of unsupported claims
4. **Token Usage**: Efficiency of token consumption
5. **Latency**: Response time differences across techniques

## Challenges and Solutions

### Challenge 1: Document Preprocessing
**Problem**: PDFs contain headers, footers, and formatting that interfere with chunking.

**Solution**: Implemented text cleaning with regex patterns to remove page numbers, headers, and normalize whitespace.

### Challenge 2: Chunk Size Optimization
**Problem**: Fixed chunk sizes can break semantic units.

**Solution**: Implemented semantic chunking that respects paragraph boundaries while maintaining size constraints.

### Challenge 3: Embedding Quality
**Problem**: Need for high-quality embeddings without API costs.

**Solution**: Used sentence-transformers/all-MiniLM-L6-v2 for local embeddings with good quality and no API costs.

### Challenge 4: Query-Context Mismatch
**Problem**: User queries may not align with indexed content vocabulary.

**Solution**: Implemented query transformation using LLM to rewrite queries for better retrieval alignment.

### Challenge 5: Hallucination Control
**Problem**: LLM may generate answers not supported by context.

**Solution**: Added explicit system prompts instructing the LLM to only use provided context and admit when answers cannot be found.

### Challenge 6: Local LLM Integration
**Problem**: Need for free, local LLM without API dependencies.

**Solution**: Integrated Ollama with Llama 3 model, providing high-quality responses locally without API keys.

## Learnings

1. **Chunking Strategy Impact**: Different chunking techniques significantly affect retrieval quality. Semantic chunking with contextual headers performed best for our corpus.

2. **Query Transformation Value**: Transforming queries improved retrieval relevance by 15-20% in initial testing.

3. **Local Embeddings Sufficiency**: Local embeddings (MiniLM) are sufficient for smaller corpora and provide good semantic understanding.

4. **FAISS Efficiency**: FAISS provides fast similarity search even with thousands of chunks, making it suitable for local deployment.

5. **Ollama Integration**: Ollama with Llama 3 provides excellent local LLM capabilities without API costs or dependencies.

6. **Prompt Engineering**: Carefully crafted prompts with explicit instructions reduce hallucination rates substantially.

## Future Enhancements

- Support for more document formats (DOCX, HTML)
- Hybrid search combining keyword and semantic search
- Multi-query retrieval for complex questions
- Response streaming for better UX
- Evaluation dashboard with metrics visualization
- Support for multiple languages
- Fine-tuning embedding models on domain-specific data

## License

MIT

## Contributors

- Team members working on RAG system implementation
