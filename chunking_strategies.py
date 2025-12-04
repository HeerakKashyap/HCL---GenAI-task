import re
from typing import List, Dict
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

class ChunkingStrategies:
    def __init__(self):
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
        
    def technique1_fixed_size_chunking(self, text: str, metadata: Dict) -> List[Dict]:
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_text = ' '.join(words[i:i + self.chunk_size])
            if chunk_text.strip():
                chunks.append({
                    'text': chunk_text,
                    'technique': 'fixed_size',
                    'metadata': metadata,
                    'chunk_index': len(chunks)
                })
        
        return chunks
    
    def technique2_semantic_chunking(self, text: str, metadata: Dict) -> List[Dict]:
        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append({
                        'text': current_chunk.strip(),
                        'technique': 'semantic',
                        'metadata': metadata,
                        'chunk_index': len(chunks)
                    })
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append({
                'text': current_chunk.strip(),
                'technique': 'semantic',
                'metadata': metadata,
                'chunk_index': len(chunks)
            })
        
        return chunks
    
    def technique3_contextual_headers(self, text: str, metadata: Dict) -> List[Dict]:
        chunks = self.technique2_semantic_chunking(text, metadata)
        
        for chunk in chunks:
            sentences = chunk['text'].split('.')
            if len(sentences) > 1:
                header = sentences[0].strip()[:100]
                chunk['header'] = header
                chunk['text'] = chunk['text']
            else:
                chunk['header'] = chunk['text'][:100]
        
        return chunks
    
    def technique4_synthetic_qa(self, text: str, metadata: Dict) -> List[Dict]:
        chunks = self.technique2_semantic_chunking(text, metadata)
        
        for chunk in chunks:
            qa_pairs = self._generate_qa_pairs(chunk['text'])
            chunk['qa_pairs'] = qa_pairs
            qa_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_pairs])
            chunk['augmented_text'] = chunk['text'] + "\n\n" + qa_text
        
        return chunks
    
    def _generate_qa_pairs(self, text: str) -> List[tuple]:
        try:
            import ollama
            use_ollama = True
        except:
            use_ollama = False
        
        if use_ollama and Config.LLM_PROVIDER == 'ollama':
            try:
                prompt = f"""Generate 2-3 question-answer pairs based on this text. Format as Q: question\nA: answer\n\nText: {text[:500]}"""
                
                response = ollama.chat(
                    model=Config.LLM_MODEL,
                    messages=[{'role': 'user', 'content': prompt}],
                    options={'temperature': 0.3, 'num_predict': 200}
                )
                
                qa_text = response['message']['content']
                qa_pairs = []
                lines = qa_text.split('\n')
                current_q = None
                
                for line in lines:
                    if line.startswith('Q:'):
                        current_q = line[2:].strip()
                    elif line.startswith('A:') and current_q:
                        qa_pairs.append((current_q, line[2:].strip()))
                        current_q = None
                
                return qa_pairs[:3]
            except Exception as e:
                print(f"Error generating QA pairs with Ollama: {e}")
                return []
        
        if openai_client and Config.OPENAI_API_KEY and Config.LLM_PROVIDER == 'openai':
            try:
                prompt = f"""Generate 2-3 question-answer pairs based on this text. Format as Q: question\nA: answer\n\nText: {text[:500]}"""
                
                response = openai_client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[{'role': 'user', 'content': prompt}],
                    temperature=0.3,
                    max_tokens=200
                )
                
                qa_text = response.choices[0].message.content
                qa_pairs = []
                lines = qa_text.split('\n')
                current_q = None
                
                for line in lines:
                    if line.startswith('Q:'):
                        current_q = line[2:].strip()
                    elif line.startswith('A:') and current_q:
                        qa_pairs.append((current_q, line[2:].strip()))
                        current_q = None
                
                return qa_pairs[:3]
            except Exception as e:
                print(f"Error generating QA pairs: {e}")
                return []
    
    def technique5_query_transformation(self, text: str, metadata: Dict) -> List[Dict]:
        chunks = self.technique2_semantic_chunking(text, metadata)
        
        for chunk in chunks:
            keywords = self._extract_keywords(chunk['text'])
            chunk['keywords'] = keywords
            chunk['transformed_queries'] = self._generate_query_variations(chunk['text'])
        
        return chunks
    
    def _extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b\w{4,}\b', text.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:10]]
    
    def _generate_query_variations(self, text: str) -> List[str]:
        sentences = text.split('.')[:3]
        variations = []
        for sent in sentences:
            if len(sent.strip()) > 20:
                variations.append(sent.strip()[:100])
        return variations[:3]
    
    def apply_all_techniques(self, documents: List[Dict]) -> List[Dict]:
        all_chunks = []
        
        for doc in documents:
            text = doc['content']
            metadata = {
                'filename': doc['filename'],
                'source': doc['source']
            }
            
            chunks_1 = self.technique1_fixed_size_chunking(text, metadata)
            chunks_2 = self.technique2_semantic_chunking(text, metadata)
            chunks_3 = self.technique3_contextual_headers(text, metadata)
            chunks_4 = self.technique4_synthetic_qa(text, metadata)
            chunks_5 = self.technique5_query_transformation(text, metadata)
            
            all_chunks.extend(chunks_1)
            all_chunks.extend(chunks_2)
            all_chunks.extend(chunks_3)
            all_chunks.extend(chunks_4)
            all_chunks.extend(chunks_5)
        
        return all_chunks

