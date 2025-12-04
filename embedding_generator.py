import os
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from config import Config

try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None
except:
    openai_client = None

class EmbeddingGenerator:
    def __init__(self):
        self.use_local = Config.USE_LOCAL_EMBEDDINGS
        self.model_name = Config.EMBEDDING_MODEL
        
        if self.use_local:
            print(f"Loading local embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        else:
            self.model = None
            if not openai_client:
                raise ValueError("OpenAI API key required for cloud embeddings")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        if self.use_local:
            return self.model.encode(text, convert_to_numpy=True)
        else:
            try:
                response = openai_client.embeddings.create(
                    model='text-embedding-ada-002',
                    input=text
                )
                return np.array(response.data[0].embedding)
            except Exception as e:
                print(f"Error generating embedding: {e}")
                raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        if self.use_local:
            return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        else:
            embeddings = []
            for text in texts:
                embedding = self.generate_embedding(text)
                embeddings.append(embedding)
            return np.array(embeddings)
    
    def generate_chunk_embeddings(self, chunks: List[Dict]) -> List[Dict]:
        texts = []
        for chunk in chunks:
            if 'augmented_text' in chunk:
                texts.append(chunk['augmented_text'])
            else:
                texts.append(chunk['text'])
        
        embeddings = self.generate_embeddings_batch(texts)
        
        for i, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[i]
        
        return chunks

