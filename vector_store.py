import os
import pickle
import numpy as np
import faiss
from typing import List, Dict
from config import Config

class VectorStore:
    def __init__(self):
        self.store_path = Config.VECTOR_DB_PATH
        self.index = None
        self.chunks = []
        self.dimension = None
        
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)
    
    def create_index(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
    
    def add_chunks(self, chunks: List[Dict]):
        if not chunks:
            return
        
        embeddings = np.array([chunk['embedding'] for chunk in chunks])
        
        if self.index is None:
            self.create_index(embeddings.shape[1])
        
        self.index.add(embeddings.astype('float32'))
        self.chunks.extend(chunks)
    
    def search(self, query_embedding: np.ndarray, top_k: int = None) -> List[Dict]:
        if self.index is None or len(self.chunks) == 0:
            return []
        
        if top_k is None:
            top_k = Config.TOP_K
        
        query_vector = query_embedding.reshape(1, -1).astype('float32')
        distances, indices = self.index.search(query_vector, min(top_k, len(self.chunks)))
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx].copy()
                chunk['similarity_score'] = float(1 / (1 + distance))
                chunk['distance'] = float(distance)
                results.append(chunk)
        
        return results
    
    def save(self, filename: str = 'vector_store'):
        index_path = os.path.join(self.store_path, f'{filename}.faiss')
        chunks_path = os.path.join(self.store_path, f'{filename}.pkl')
        
        if self.index is not None:
            faiss.write_index(self.index, index_path)
        
        with open(chunks_path, 'wb') as f:
            pickle.dump(self.chunks, f)
    
    def load(self, filename: str = 'vector_store'):
        index_path = os.path.join(self.store_path, f'{filename}.faiss')
        chunks_path = os.path.join(self.store_path, f'{filename}.pkl')
        
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        
        if os.path.exists(chunks_path):
            with open(chunks_path, 'rb') as f:
                self.chunks = pickle.load(f)
                if self.chunks and 'embedding' in self.chunks[0]:
                    self.dimension = len(self.chunks[0]['embedding'])
    
    def get_stats(self) -> Dict:
        return {
            'total_chunks': len(self.chunks),
            'dimension': self.dimension,
            'indexed': self.index is not None
        }

