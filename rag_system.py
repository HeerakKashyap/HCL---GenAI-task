import os
from document_processor import DocumentProcessor
from chunking_strategies import ChunkingStrategies
from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore
from config import Config

class RAGSystem:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.chunking_strategies = ChunkingStrategies()
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.initialized = False
    
    def initialize(self, force_rebuild: bool = False):
        if not force_rebuild:
            try:
                self.vector_store.load()
                if len(self.vector_store.chunks) > 0:
                    self.initialized = True
                    print("Loaded existing vector store")
                    return
            except Exception as e:
                print(f"Could not load existing store: {e}")
        
        print("Building vector store from documents...")
        documents = self.document_processor.load_documents()
        
        if not documents:
            print("No documents found. Please add PDF or TXT files to the documents/ directory.")
            return
        
        print(f"Processing {len(documents)} documents...")
        chunks = self.chunking_strategies.apply_all_techniques(documents)
        print(f"Generated {len(chunks)} chunks using 5 RAG techniques")
        
        print("Generating embeddings...")
        chunks_with_embeddings = self.embedding_generator.generate_chunk_embeddings(chunks)
        
        print("Indexing vectors...")
        self.vector_store.add_chunks(chunks_with_embeddings)
        self.vector_store.save()
        
        self.initialized = True
        print(f"Vector store initialized with {len(self.vector_store.chunks)} chunks")
    
    def get_stats(self):
        return self.vector_store.get_stats()

