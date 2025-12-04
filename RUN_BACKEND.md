# How to Run the Backend

## Important: Always Activate Virtual Environment First!

### Step 1: Activate Virtual Environment
```bash
venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### Step 2: Start Backend
```bash
python app.py
```

### What You Should See:

```
Loading local embedding model: sentence-transformers/all-MiniLM-L6-v2
Building vector store from documents...
Processing 5 documents...
Generated 28 chunks using 5 RAG techniques
Generating embeddings...
Batches: 100%|████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.39it/s]
Indexing vectors...
Vector store initialized with 28 chunks
Loading local embedding model: sentence-transformers/all-MiniLM-L6-v2
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### If You See Errors:

**Error: "ModuleNotFoundError: No module named 'flask_cors'"**
- Solution: Make sure venv is activated, then run: `pip install -r requirements.txt`

**Error: "No documents found"**
- Solution: Make sure you have files in the `documents/` folder

**Error: Port already in use**
- Solution: Close other applications using port 5000, or change port in app.py

### Quick Test:

Once backend is running, open a NEW terminal and run:
```bash
python test_api.py
```

Or open browser: http://localhost:5000/api/health

