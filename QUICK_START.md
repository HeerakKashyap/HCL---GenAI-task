# Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key (optional, for cloud features)

## Installation Steps

1. Create and activate virtual environment:

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

2. Upgrade pip:
```bash
python -m pip install --upgrade pip
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd client
npm install
cd ..
```

3. Set up environment:
```bash
python run.py
```

4. Add your documents:
   - Place 3-5 PDF or TXT files in the `documents/` directory
   - Or use the provided sample document

5. Configure API key (optional):
   - Edit `.env` file
   - Add your `OPENAI_API_KEY` if you want to use cloud embeddings or LLM features

## Running the Application

**Important:** Make sure your virtual environment is activated before running Python commands.

### Start Backend
```bash
python app.py
```
Backend runs on http://localhost:5000

### Start Frontend (in new terminal)
```bash
cd client
npm start
```
Frontend runs on http://localhost:3000

## First Query

1. Open http://localhost:3000 in your browser
2. Enter a question about your documents
3. Click "Ask" to get the answer
4. View sources and similarity scores

## Rebuilding Vector Store

If you add new documents, click "Rebuild Index" in the UI or call:
```bash
curl -X POST http://localhost:5000/api/rebuild
```

## Testing API

```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "use_transformation": true}'
```

