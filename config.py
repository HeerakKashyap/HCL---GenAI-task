import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './vector_store')
    DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', './documents')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 500))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))
    TOP_K = int(os.getenv('TOP_K', 3))
    USE_LOCAL_EMBEDDINGS = os.getenv('USE_LOCAL_EMBEDDINGS', 'true').lower() == 'true'
    USE_LOCAL_LLM = os.getenv('USE_LOCAL_LLM', 'false').lower() == 'true'

