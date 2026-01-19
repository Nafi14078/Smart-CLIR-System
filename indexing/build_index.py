"""
Indexing and Preprocessing Module for CLIR System
Builds inverted index for BM25 retrieval and preprocesses documents
"""

import json
import pickle
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import numpy as np
from tqdm import tqdm


class DocumentPreprocessor:
    """Handles text preprocessing for both Bangla and English"""
    
    def __init__(self):
        # English stopwords
        self.english_stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have', 'had',
            'what', 'when', 'where', 'who', 'which', 'why', 'how'
        }
        
        # Common Bangla stopwords
        self.bangla_stopwords = {
            'এবং', 'বা', 'যে', 'এই', 'সেই', 'যা', 'তা', 'এক', 'একটি',
            'কিছু', 'কোন', 'করা', 'হয়', 'হবে', 'ছিল', 'আছে', 'থেকে',
            'সঙ্গে', 'দ্বারা', 'জন্য', 'মধ্যে', 'উপর', 'নিচে', 'আগে',
            'পরে', 'মত', 'সাথে', 'কিন্তু', 'যদি', 'তবে', 'না', 'নয়',
            'হয়েছে', 'হয়েছিল', 'করেছে', 'করেছিল', 'বলেন', 'বলে',
            'বলা', 'জানা', 'জানায়', 'দেয়', 'দেওয়া', 'নেয়', 'নেওয়া'
        }
    
    def is_bangla(self, text: str) -> bool:
        """Check if text contains Bangla characters"""
        bangla_pattern = re.compile(r'[\u0980-\u09FF]')
        return bool(bangla_pattern.search(text))
    
    def tokenize(self, text: str, language: str = 'auto') -> List[str]:
        """Tokenize text into words"""
        if language == 'auto':
            language = 'bn' if self.is_bangla(text) else 'en'
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # For Bangla, keep Bangla characters and spaces
        if language == 'bn':
            # Keep Bangla Unicode range
            text = re.sub(r'[^\u0980-\u09FF\s]', ' ', text)
        else:
            # For English, keep only alphanumeric and spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Split into tokens and filter empty strings
        tokens = [t.strip() for t in text.lower().split() if t.strip()]
        
        return tokens
    
    def remove_stopwords(self, tokens: List[str], language: str = 'auto') -> List[str]:
        """Remove stopwords from token list"""
        if language == 'auto':
            # Detect language from first token
            language = 'bn' if tokens and self.is_bangla(tokens[0]) else 'en'
        
        stopwords = self.bangla_stopwords if language == 'bn' else self.english_stopwords
        return [t for t in tokens if t not in stopwords]
    
    def preprocess(self, text: str, language: str = 'auto') -> List[str]:
        """Complete preprocessing pipeline"""
        if not text or not isinstance(text, str):
            return []
        
        tokens = self.tokenize(text, language)
        tokens = self.remove_stopwords(tokens, language)
        
        # Filter very short tokens (likely noise)
        tokens = [t for t in tokens if len(t) > 1]
        
        return tokens


class InvertedIndex:
    """Inverted index for efficient document retrieval"""
    
    def __init__(self):
        self.index = defaultdict(list)  # term -> [(doc_id, term_freq), ...]
        self.doc_lengths = {}  # doc_id -> document length
        self.doc_count = 0
        self.avg_doc_length = 0
        self.term_doc_freq = defaultdict(int)  # term -> number of docs containing term
        self.documents = {}  # doc_id -> document metadata
        
    def add_document(self, doc_id: str, tokens: List[str], metadata: Dict):
        """Add a document to the index"""
        # Count term frequencies
        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1
        
        # Add to inverted index
        for term, freq in term_freq.items():
            self.index[term].append((doc_id, freq))
            self.term_doc_freq[term] += 1
        
        # Store document metadata
        doc_length = len(tokens)
        self.doc_lengths[doc_id] = doc_length
        self.documents[doc_id] = metadata
        self.doc_count += 1
    
    def finalize(self):
        """Calculate statistics after all documents are added"""
        if self.doc_count > 0:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.doc_count
        
        print(f"Index built with {self.doc_count} documents")
        print(f"Vocabulary size: {len(self.index)}")
        print(f"Average document length: {self.avg_doc_length:.2f} tokens")
    
    def get_postings(self, term: str) -> List[Tuple[str, int]]:
        """Get posting list for a term"""
        return self.index.get(term, [])
    
    def get_document_frequency(self, term: str) -> int:
        """Get number of documents containing the term"""
        return self.term_doc_freq.get(term, 0)
    
    def save(self, filepath: str):
        """Save index to disk"""
        data = {
            'index': dict(self.index),
            'doc_lengths': self.doc_lengths,
            'doc_count': self.doc_count,
            'avg_doc_length': self.avg_doc_length,
            'term_doc_freq': dict(self.term_doc_freq),
            'documents': self.documents
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Index saved to {filepath}")
    
    @staticmethod
    def load(filepath: str) -> 'InvertedIndex':
        """Load index from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        index = InvertedIndex()
        index.index = defaultdict(list, data['index'])
        index.doc_lengths = data['doc_lengths']
        index.doc_count = data['doc_count']
        index.avg_doc_length = data['avg_doc_length']
        index.term_doc_freq = defaultdict(int, data['term_doc_freq'])
        index.documents = data['documents']
        
        print(f"Index loaded from {filepath}")
        print(f"Documents: {index.doc_count}, Vocabulary: {len(index.index)}")
        
        return index


def load_documents(json_path: str) -> List[Dict]:
    """Load documents from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    return documents


def build_index_from_documents(documents: List[Dict], language: str, 
                               preprocessor: DocumentPreprocessor) -> InvertedIndex:
    """Build inverted index from document list"""
    index = InvertedIndex()
    
    print(f"Building index for {len(documents)} {language} documents...")
    
    for i, doc in enumerate(tqdm(documents, desc=f"Indexing {language} docs")):
        # Create unique document ID
        doc_id = f"{language}_{i}"
        
        # Combine title and body for indexing
        text = f"{doc.get('title', '')} {doc.get('body', '')}"
        
        # Preprocess text
        tokens = preprocessor.preprocess(text, language)
        
        # Store metadata
        metadata = {
            'title': doc.get('title', ''),
            'url': doc.get('url', ''),
            'language': language,
            'original_index': i
        }
        
        # Add to index
        index.add_document(doc_id, tokens, metadata)
    
    index.finalize()
    return index


def build_combined_index(bangla_json: str, english_json: str, output_dir: str):
    """Build combined index for both languages"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    preprocessor = DocumentPreprocessor()
    
    # Load documents
    print("Loading documents...")
    bangla_docs = load_documents(bangla_json)
    english_docs = load_documents(english_json)
    
    print(f"Loaded {len(bangla_docs)} Bangla and {len(english_docs)} English documents")
    
    # Build separate indices for each language
    bangla_index = build_index_from_documents(bangla_docs, 'bn', preprocessor)
    english_index = build_index_from_documents(english_docs, 'en', preprocessor)
    
    # Save indices
    bangla_index.save(str(output_path / 'bangla_index.pkl'))
    english_index.save(str(output_path / 'english_index.pkl'))
    
    # Build combined index
    print("\nBuilding combined index...")
    combined_index = InvertedIndex()
    
    # Add all Bangla documents
    for doc_id, metadata in tqdm(bangla_index.documents.items(), desc="Adding Bangla docs"):
        # Reconstruct tokens from index
        tokens = []
        for term, postings in bangla_index.index.items():
            for posting_doc_id, freq in postings:
                if posting_doc_id == doc_id:
                    tokens.extend([term] * freq)
        combined_index.add_document(doc_id, tokens, metadata)
    
    # Add all English documents
    for doc_id, metadata in tqdm(english_index.documents.items(), desc="Adding English docs"):
        # Reconstruct tokens from index
        tokens = []
        for term, postings in english_index.index.items():
            for posting_doc_id, freq in postings:
                if posting_doc_id == doc_id:
                    tokens.extend([term] * freq)
        combined_index.add_document(doc_id, tokens, metadata)
    
    combined_index.finalize()
    combined_index.save(str(output_path / 'combined_index.pkl'))
    
    print("\n✅ Index building complete!")
    print(f"Indices saved in: {output_dir}")
    
    return bangla_index, english_index, combined_index


if __name__ == "__main__":
    # Build indices
    bangla_json = "data/processed/bangla_docs.json"
    english_json = "data/processed/english_docs.json"
    output_dir = "data/indices"
    
    build_combined_index(bangla_json, english_json, output_dir)
