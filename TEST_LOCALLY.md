# Testing the RAG System Locally

## Quick Start

### Option 1: Using Batch Files (Easiest)

1. **Start Backend:**
   - Double-click `start_backend.bat`
   - Wait for "Vector store initialized" message
   - Server runs on http://localhost:5000

2. **Start Frontend (New Terminal/Window):**
   - Double-click `start_frontend.bat`
   - Browser opens to http://localhost:3000

### Option 2: Manual Commands

**Terminal 1 - Backend:**
```bash
venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd client
npm start
```

## Testing Steps

### 1. Check Backend is Running

Open browser: http://localhost:5000/api/health

Expected response:
```json
{
  "status": "OK",
  "initialized": true,
  "stats": {
    "total_chunks": 28,
    "dimension": 384,
    "indexed": true
  }
}
```

### 2. Test API with curl

```bash
curl -X POST http://localhost:5000/api/query -H "Content-Type: application/json" -d "{\"query\": \"What is RAG?\"}"
```

### 3. Test via Python Script

```bash
python test_api.py
```

### 4. Use Web Interface

1. Open http://localhost:3000
2. Enter query: "What is RAG?"
3. Click "Ask"
4. View answer, sources, and token usage

## Test Queries to Try

- "What is RAG?"
- "Explain machine learning"
- "What are vector databases?"
- "How do embeddings work?"
- "Describe artificial intelligence"

## Troubleshooting

**Backend won't start:**
- Make sure virtual environment is activated
- Check if port 5000 is already in use
- Verify all packages are installed: `pip install -r requirements.txt`

**Frontend won't connect:**
- Ensure backend is running first
- Check browser console for errors
- Verify API URL in client code

**No answers generated:**
- Check if documents are in `documents/` folder
- Verify vector store was built (check backend logs)
- Ensure OpenAI API key is set if using cloud features

