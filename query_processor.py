from typing import List, Dict
from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore
from config import Config

try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY and Config.LLM_PROVIDER == 'openai' else None
except:
    openai_client = None

try:
    import ollama
    ollama_available = True
except:
    ollama_available = False

class QueryProcessor:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.use_local_llm = Config.USE_LOCAL_LLM
    
    def transform_query(self, query: str) -> str:
        if Config.LLM_PROVIDER == 'ollama' and ollama_available:
            try:
                prompt = f"""Rewrite this query to improve retrieval from a document corpus. Keep the core meaning but make it more specific and searchable.

Original query: {query}
Rewritten query:"""
                
                response = ollama.chat(
                    model=Config.LLM_MODEL,
                    messages=[{'role': 'user', 'content': prompt}],
                    options={'temperature': 0.3, 'num_predict': 100}
                )
                
                transformed = response['message']['content'].strip()
                return transformed if transformed else query
            except Exception as e:
                print(f"Query transformation error: {e}")
                return query
        elif openai_client and Config.OPENAI_API_KEY:
            try:
                prompt = f"""Rewrite this query to improve retrieval from a document corpus. Keep the core meaning but make it more specific and searchable.

Original query: {query}
Rewritten query:"""
                
                response = openai_client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[{'role': 'user', 'content': prompt}],
                    temperature=0.3,
                    max_tokens=100
                )
                
                transformed = response.choices[0].message.content.strip()
                return transformed if transformed else query
            except Exception as e:
                print(f"Query transformation error: {e}")
                return query
        else:
            return query
    
    def retrieve_context(self, query_embedding, top_k: int = None) -> List[Dict]:
        results = self.vector_store.search(query_embedding, top_k)
        return results
    
    def generate_response(self, query: str, context_chunks: List[Dict]) -> Dict:
        context_text = "\n\n".join([
            f"[Source: {chunk.get('metadata', {}).get('filename', 'unknown')}]\n{chunk.get('text', '')}"
            for chunk in context_chunks[:Config.TOP_K]
        ])
        
        system_prompt = """You are a helpful assistant that answers questions based only on the provided context. 
If the answer cannot be found in the context, say so. Do not make up information."""
        
        user_prompt = f"""Context:
{context_text}

Question: {query}

Answer based only on the context provided:"""
        
        if not context_chunks:
            return {
                'answer': 'No relevant information found in the documents. Please try a different query.',
                'sources': [],
                'tokens_used': {},
                'chunks_retrieved': 0
            }
        
        if Config.LLM_PROVIDER == 'ollama' and ollama_available:
            try:
                response = ollama.chat(
                    model=Config.LLM_MODEL,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt}
                    ],
                    options={'temperature': 0.3, 'num_predict': 500}
                )
                
                answer = response['message']['content']
                
                sources = []
                for chunk in context_chunks:
                    source_info = {
                        'filename': chunk.get('metadata', {}).get('filename', 'unknown'),
                        'similarity': chunk.get('similarity_score', 0),
                        'technique': chunk.get('technique', 'unknown')
                    }
                    sources.append(source_info)
                
                return {
                    'answer': answer,
                    'sources': sources,
                    'tokens_used': {
                        'prompt_tokens': response.get('prompt_eval_count', 0),
                        'completion_tokens': response.get('eval_count', 0),
                        'total_tokens': response.get('prompt_eval_count', 0) + response.get('eval_count', 0)
                    },
                    'chunks_retrieved': len(context_chunks)
                }
            except Exception as e:
                print(f"Ollama error: {e}")
                return {
                    'answer': f"Error generating response: {str(e)}. Make sure Ollama is running and model is installed.",
                    'sources': [],
                    'tokens_used': {},
                    'chunks_retrieved': 0
                }
        elif openai_client and Config.LLM_PROVIDER == 'openai':
            try:
                response = openai_client.chat.completions.create(
                    model=Config.LLM_MODEL,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                answer = response.choices[0].message.content
                usage = response.usage
                
                sources = []
                for chunk in context_chunks:
                    source_info = {
                        'filename': chunk.get('metadata', {}).get('filename', 'unknown'),
                        'similarity': chunk.get('similarity_score', 0),
                        'technique': chunk.get('technique', 'unknown')
                    }
                    sources.append(source_info)
                
                return {
                    'answer': answer,
                    'sources': sources,
                    'tokens_used': {
                        'prompt_tokens': usage.prompt_tokens,
                        'completion_tokens': usage.completion_tokens,
                        'total_tokens': usage.total_tokens
                    },
                    'chunks_retrieved': len(context_chunks)
                }
            except Exception as e:
                return {
                    'answer': f"Error generating response: {str(e)}",
                    'sources': [],
                    'tokens_used': {},
                    'chunks_retrieved': 0
                }
        else:
            answer_parts = []
            for i, chunk in enumerate(context_chunks[:Config.TOP_K], 1):
                chunk_text = chunk.get('text', '')
                if chunk_text:
                    answer_parts.append(f"[Source {i}: {chunk.get('metadata', {}).get('filename', 'unknown')}]\n{chunk_text}")
            
            return {
                'answer': '\n\n'.join(answer_parts),
                'sources': [{
                    'filename': chunk.get('metadata', {}).get('filename', 'unknown'),
                    'similarity': chunk.get('similarity_score', 0),
                    'technique': chunk.get('technique', 'unknown')
                } for chunk in context_chunks],
                'tokens_used': {
                    'prompt_tokens': 0,
                    'completion_tokens': 0,
                    'total_tokens': 0
                },
                'chunks_retrieved': len(context_chunks)
            }
    
    def process_query(self, query: str, use_transformation: bool = True) -> Dict:
        transformed_query = self.transform_query(query) if use_transformation else query
        
        query_embedding = self.embedding_generator.generate_embedding(transformed_query)
        
        context_chunks = self.retrieve_context(query_embedding)
        
        response = self.generate_response(query, context_chunks)
        response['transformed_query'] = transformed_query if use_transformation else query
        
        return response

