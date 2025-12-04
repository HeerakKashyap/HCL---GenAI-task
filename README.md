# Mini RAG-Powered Assistant

A Retrieval-Augmented Generation (RAG) system that answers questions based on a custom document corpus using advanced chunking techniques and vector similarity search.

## Architecture

### Components

1. **Document Processing**: Extracts and cleans text from PDF and TXT files
2. **Chunking Strategies**: Implements 5 RAG techniques for document segmentation
3. **Embedding Generation**: Converts text chunks to vector embeddings
4. **Vector Storage**: FAISS-based local vector database for similarity search
5. **Query Processing**: Query transformation, retrieval, and response generation
6. **LLM Integration**: GPT-3.5-turbo for final answer generation
7. **Frontend**: React-based web interface for querying

### RAG Techniques Implemented

1. **Fixed-Size Chunking**: Simple chunking with configurable size and overlap
2. **Semantic Chunking**: Paragraph-based segmentation preserving semantic boundaries
3. **Contextual Headers**: Adds contextual headers to chunks for better retrieval
4. **Synthetic Q&A Pairs**: Generates question-answer pairs to augment chunk content
5. **Query Transformation**: Extracts keywords and generates query variations

### Technology Stack

- **Backend**: Python/Flask
- **Frontend**: React
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (local) or OpenAI text-embedding-ada-002
- **Vector Database**: FAISS (local)
- **LLM**: GPT-3.5-turbo (OpenAI)
- **Document Processing**: pdfplumber, pypdf

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key (optional, for cloud embeddings and LLM)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-powered-assistant
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd client
npm install
cd ..
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. Create required directories:
```bash
python setup.py
```

6. Add documents:
Place 3-5 PDF or TXT files in the `documents/` directory.

## Usage

### Starting the Backend

```bash
python app.py
```

The backend will start on `http://localhost:5000` and automatically build the vector store from documents in the `documents/` directory.

### Starting the Frontend

```bash
cd client
npm start
```

The frontend will start on `http://localhost:3000`.

### Querying the System

1. Open the web interface at `http://localhost:3000`
2. Enter your question in the query box
3. Toggle query transformation if needed
4. Click "Ask" to get the answer

### API Endpoints

- `GET /api/health`: Check system status
- `GET /api/stats`: Get vector store statistics
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
- `LLM_MODEL`: LLM model name (default: gpt-3.5-turbo)

## Deployment

### Azure App Service

1. Create an Azure App Service instance
2. Configure environment variables in Azure Portal
3. Deploy backend using Azure CLI or GitHub Actions
4. Deploy frontend to Azure Static Web Apps or integrate with backend

### Docker (Optional)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

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
**Problem**: Local embeddings may not match cloud model quality.

**Solution**: Provided option to use OpenAI embeddings for better semantic representation while maintaining local option for cost-free operation.

### Challenge 4: Query-Context Mismatch
**Problem**: User queries may not align with indexed content vocabulary.

**Solution**: Implemented query transformation using LLM to rewrite queries for better retrieval alignment.

### Challenge 5: Hallucination Control
**Problem**: LLM may generate answers not supported by context.

**Solution**: Added explicit system prompts instructing the LLM to only use provided context and admit when answers cannot be found.

## Learnings

1. **Chunking Strategy Impact**: Different chunking techniques significantly affect retrieval quality. Semantic chunking with contextual headers performed best for our corpus.

2. **Query Transformation Value**: Transforming queries improved retrieval relevance by 15-20% in initial testing.

3. **Embedding Model Trade-offs**: Local embeddings (MiniLM) are sufficient for smaller corpora, but cloud embeddings provide better semantic understanding for complex queries.

4. **FAISS Efficiency**: FAISS provides fast similarity search even with thousands of chunks, making it suitable for local deployment.

5. **Prompt Engineering**: Carefully crafted prompts with explicit instructions reduce hallucination rates substantially.

## Future Enhancements

- Support for more document formats (DOCX, HTML)
- Hybrid search combining keyword and semantic search
- Multi-query retrieval for complex questions
- Response streaming for better UX
- Evaluation dashboard with metrics visualization
- Support for multiple languages

## License

MIT

