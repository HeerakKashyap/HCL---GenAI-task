# Setup Ollama for RAG System

## Step 1: Install Ollama

1. Download from: https://ollama.ai
2. Install the application
3. Ollama will run as a service in the background

## Step 2: Pull Llama Model

Open terminal and run:

```bash
ollama pull llama3
```

This downloads the Llama 3 model (about 4.7GB). Takes 5-10 minutes depending on internet speed.

**Alternative models (smaller/faster):**
```bash
ollama pull llama3.2    # Smaller, faster
ollama pull mistral     # Alternative option
```

## Step 3: Install Python Package

```bash
venv\Scripts\activate
pip install ollama
```

## Step 4: Verify Installation

Test if Ollama is working:

```bash
python -c "import ollama; print(ollama.chat(model='llama3', messages=[{'role': 'user', 'content': 'Hello'}]))"
```

## Step 5: Restart Backend

```bash
venv\Scripts\activate
python app.py
```

## Configuration

The system is configured to use:
- **LLM Provider:** Ollama (default)
- **LLM Model:** llama3 (default)

You can change in `.env` file:
```
LLM_PROVIDER=ollama
LLM_MODEL=llama3
```

## Troubleshooting

**Error: "Connection refused"**
- Make sure Ollama is running
- Check: `ollama list` should show your models

**Error: "Model not found"**
- Run: `ollama pull llama3`

**Slow responses**
- Use smaller model: `llama3.2` or `mistral`
- Or use GPU if available

**To switch back to OpenAI:**
- Set in `.env`: `LLM_PROVIDER=openai`
- Add: `OPENAI_API_KEY=your_key`

