# Running and Testing the RAG System

## Step-by-Step Guide

### Step 1: Set Up Directories and Documents

1. Create required directories:
```bash
python setup.py
```

2. Add documents to the `documents/` folder:
   - Copy 3-5 PDF or TXT files into the `documents/` directory
   - Or use the sample document that was created
   - Example: Copy `sample_document.txt` to `documents/` if not already there

### Step 2: Configure Environment (Optional)

1. Create `.env` file if not exists:
```bash
copy .env.example .env
```

2. Edit `.env` and add your OpenAI API key (if you want to use cloud features):
```
OPENAI_API_KEY=your_key_here
```

**Note:** The system works without API key using local embeddings, but Q&A generation and query transformation will be limited.

### Step 3: Start the Backend Server

In your terminal (with venv activated):
```bash
python app.py
```

**Expected Output:**
```
Building vector store from documents...
Processing 1 documents...
Generated 25 chunks using 5 RAG techniques
Generating embeddings...
Indexing vectors...
Vector store initialized with 25 chunks
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
```

**What's happening:**
- System loads documents from `documents/` folder
- Applies 5 chunking techniques to each document
- Generates embeddings for all chunks
- Creates FAISS vector index
- Starts Flask server on port 5000

### Step 4: Start the Frontend (New Terminal)

Open a NEW terminal window, activate venv, then:
```bash
cd client
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view rag-client in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

The browser should automatically open to `http://localhost:3000`

### Step 5: Using the Web Interface

**What you'll see:**
- Header: "RAG-Powered Assistant"
- Stats panel showing: Number of chunks and dimension
- Query input box
- Checkbox for "Enable Query Transformation"
- "Rebuild Index" button

**To test the system:**

1. **Enter a query** in the input box, for example:
   - "What is RAG?"
   - "Explain machine learning"
   - "What are embeddings?"
   - "How does vector database work?"

2. **Click "Ask"** button

3. **Expected Response Structure:**
   ```
   Answer:
   [The generated answer based on your documents]
   
   Transformed Query: (if transformation enabled)
   [Rewritten version of your query]
   
   Sources (3):
   - filename.pdf
     Technique: semantic
     Similarity: 85.23%
   
   Token Usage:
   Prompt: 450 tokens
   Completion: 120 tokens
   Total: 570 tokens
   ```

### Step 6: Test via API (Alternative)

You can also test using curl or Postman:

```bash
curl -X POST http://localhost:5000/api/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"What is RAG?\", \"use_transformation\": true}"
```

**Expected JSON Response:**
```json
{
  "answer": "Retrieval-Augmented Generation (RAG) is a technique...",
  "sources": [
    {
      "filename": "sample_document.txt",
      "similarity": 0.8523,
      "technique": "semantic"
    }
  ],
  "tokens_used": {
    "prompt_tokens": 450,
    "completion_tokens": 120,
    "total_tokens": 570
  },
  "chunks_retrieved": 3,
  "transformed_query": "What is Retrieval-Augmented Generation and how does it work?"
}
```

## What to Expect

### Input Examples:

**Good Queries:**
- "What is artificial intelligence?"
- "Explain how embeddings work"
- "What are the benefits of RAG?"
- "Describe machine learning"

**What Happens Behind the Scenes:**
1. Query is optionally transformed for better retrieval
2. Query is converted to embedding vector
3. System searches vector database for similar chunks
4. Top 3 most relevant chunks are retrieved
5. Chunks are passed to LLM with your query
6. LLM generates answer based only on retrieved context

### Output Characteristics:

**Successful Response:**
- Answer directly addresses your question
- Answer is based on document content
- Sources show which documents were used
- Similarity scores indicate relevance (higher is better)
- Token usage shows API consumption

**If Answer Not Found:**
- LLM will say "I cannot find the answer in the provided context"
- This prevents hallucination
- Sources may have low similarity scores

**Error Scenarios:**
- "RAG system not initialized" - No documents loaded
- "OpenAI API key not configured" - Need API key for LLM
- Empty response - Check backend logs

## Testing Different Features

### Test Query Transformation:
1. Enter query: "ML"
2. Check "Enable Query Transformation"
3. Submit
4. See "Transformed Query" showing expanded version like "machine learning"

### Test Without Transformation:
1. Uncheck "Enable Query Transformation"
2. Submit same query
3. No transformed query shown

### Test Rebuild:
1. Add new document to `documents/` folder
2. Click "Rebuild Index" button
3. Wait for processing
4. Stats update with new chunk count

## Troubleshooting

**Backend won't start:**
- Check if port 5000 is already in use
- Verify all packages installed correctly
- Check for documents in `documents/` folder

**Frontend won't connect:**
- Ensure backend is running first
- Check CORS settings
- Verify API URL in frontend code

**No answers generated:**
- Check OpenAI API key in `.env`
- Verify documents contain relevant content
- Check backend terminal for error messages

**Empty vector store:**
- Ensure documents are in `documents/` folder
- Check file formats (PDF or TXT only)
- Run `python setup.py` to create directories

## Next Steps After Testing

1. Add your own documents (PDFs or TXT files)
2. Rebuild the index
3. Test with domain-specific queries
4. Compare results with/without query transformation
5. Review source citations for accuracy

