import os
import pdfplumber
import pypdf
import re
from typing import List, Dict
from config import Config

class DocumentProcessor:
    def __init__(self):
        self.documents_path = Config.DOCUMENTS_PATH
        
    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_txt(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\'\"\n]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d+/\d+', '', text)
        return text.strip()
    
    def load_documents(self) -> List[Dict[str, str]]:
        documents = []
        if not os.path.exists(self.documents_path):
            os.makedirs(self.documents_path)
            print(f"Created documents directory: {self.documents_path}")
            return documents
        
        for filename in os.listdir(self.documents_path):
            file_path = os.path.join(self.documents_path, filename)
            if filename.endswith('.pdf'):
                text = self.extract_text_from_pdf(file_path)
            elif filename.endswith('.txt'):
                text = self.extract_text_from_txt(file_path)
            else:
                continue
            
            if text:
                cleaned_text = self.clean_text(text)
                documents.append({
                    'filename': filename,
                    'content': cleaned_text,
                    'source': file_path
                })
        
        return documents

