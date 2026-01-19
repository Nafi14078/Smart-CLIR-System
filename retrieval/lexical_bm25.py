"""
BM25 Lexical Retrieval Model
Implements the BM25 ranking algorithm for document retrieval
"""

import math
import time
from typing import List, Dict, Tuple
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from indexing.build_index import InvertedIndex, DocumentPreprocessor


class BM25Retriever:
    """BM25 ranking algorithm implementation"""
    
    def __init__(self, index_path: str = None, k1: float = 1.5, b: float = 0.75):
        """
        Initialize BM25 retriever
        
        Args:
            index_path: Path to the inverted index file
            k1: Term frequency saturation parameter (default: 1.5)
            b: Length normalization parameter (default: 0.75)
        """
        self.k1 = k1
        self.b = b
        self.preprocessor = DocumentPreprocessor()
        self.index = None
        
        if index_path:
            self.load_index(index_path)
    
    def load_index(self, index_path: str):
        """Load inverted index from file"""
        self.index = InvertedIndex.load(index_path)
        print(f"BM25 Retriever ready with {self.index.doc_count} documents")
    
    def compute_idf(self, term: str) -> float:
        """
        Compute IDF (Inverse Document Frequency) for a term
        IDF = log((N - df + 0.5) / (df + 0.5))
        where N is total documents and df is document frequency
        """
        if not self.index:
            return 0.0
        
        N = self.index.doc_count
        df = self.index.get_document_frequency(term)
        
        if df == 0:
            return 0.0
        
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
        return idf
    
    def compute_bm25_score(self, query_terms: List[str], doc_id: str) -> float:
        """
        Compute BM25 score for a document given query terms
        
        BM25(q,d) = Σ IDF(qi) × (f(qi,d) × (k1+1)) / (f(qi,d) + k1 × (1-b+b×|d|/avgdl))
        """
        if not self.index:
            return 0.0
        
        score = 0.0
        doc_length = self.index.doc_lengths.get(doc_id, 0)
        
        if doc_length == 0:
            return 0.0
        
        avgdl = self.index.avg_doc_length
        
        for term in query_terms:
            # Get IDF
            idf = self.compute_idf(term)
            
            if idf == 0:
                continue
            
            # Get term frequency in document
            tf = 0
            postings = self.index.get_postings(term)
            for posting_doc_id, freq in postings:
                if posting_doc_id == doc_id:
                    tf = freq
                    break
            
            if tf == 0:
                continue
            
            # Compute BM25 component
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / avgdl))
            
            score += idf * (numerator / denominator)
        
        return score
    
    def search(self, query: str, top_k: int = 10, language: str = 'auto') -> Dict:
        """
        Search for documents matching the query
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            language: Language of query ('en', 'bn', or 'auto')
        
        Returns:
            Dictionary with results and timing information
        """
        if not self.index:
            raise ValueError("Index not loaded. Call load_index() first.")
        
        start_time = time.time()
        
        # Preprocess query
        preprocess_start = time.time()
        query_terms = self.preprocessor.preprocess(query, language)
        preprocess_time = time.time() - preprocess_start
        
        if not query_terms:
            return {
                'query': query,
                'results': [],
                'total_results': 0,
                'timing': {
                    'total': 0,
                    'preprocessing': preprocess_time,
                    'search': 0
                }
            }
        
        # Get candidate documents (documents containing at least one query term)
        search_start = time.time()
        candidate_docs = set()
        for term in query_terms:
            postings = self.index.get_postings(term)
            for doc_id, _ in postings:
                candidate_docs.add(doc_id)
        
        # Score all candidate documents
        scored_docs = []
        for doc_id in candidate_docs:
            score = self.compute_bm25_score(query_terms, doc_id)
            if score > 0:
                metadata = self.index.documents[doc_id]
                scored_docs.append({
                    'doc_id': doc_id,
                    'score': score,
                    'title': metadata['title'],
                    'url': metadata['url'],
                    'language': metadata['language']
                })
        
        # Sort by score (descending)
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        
        # Take top-k results
        top_results = scored_docs[:top_k]
        
        # Add confidence scores (normalized scores)
        if top_results:
            max_score = top_results[0]['score']
            for result in top_results:
                # Normalize score to [0, 1]
                result['confidence'] = result['score'] / max_score if max_score > 0 else 0
                
                # Add caution flag for low confidence
                result['caution'] = result['confidence'] < 0.3
        
        search_time = time.time() - search_start
        total_time = time.time() - start_time
        
        return {
            'query': query,
            'query_terms': query_terms,
            'results': top_results,
            'total_results': len(scored_docs),
            'timing': {
                'total': total_time,
                'preprocessing': preprocess_time,
                'search': search_time
            }
        }
    
    def print_results(self, search_results: Dict):
        """Pretty print search results"""
        print(f"\n{'='*80}")
        print(f"Query: {search_results['query']}")
        print(f"Query Terms: {', '.join(search_results['query_terms'])}")
        print(f"Total Results: {search_results['total_results']}")
        print(f"{'='*80}\n")
        
        for i, result in enumerate(search_results['results'], 1):
            print(f"{i}. [{result['language'].upper()}] {result['title']}")
            print(f"   Score: {result['score']:.4f} | Confidence: {result['confidence']:.2%}")
            
            if result['caution']:
                print(f"   ⚠️  CAUTION: Low confidence result")
            
            print(f"   URL: {result['url']}")
            print()
        
        print(f"{'='*80}")
        print(f"Timing:")
        print(f"  Preprocessing: {search_results['timing']['preprocessing']*1000:.2f}ms")
        print(f"  Search: {search_results['timing']['search']*1000:.2f}ms")
        print(f"  Total: {search_results['timing']['total']*1000:.2f}ms")
        print(f"{'='*80}\n")


def main():
    """Test BM25 retrieval"""
    # Load index
    index_path = "data/indices/combined_index.pkl"
    retriever = BM25Retriever(index_path)
    
    # Test queries
    test_queries = [
        "Bangladesh politics",
        "বাংলাদেশ রাজনীতি",
        "cricket sports",
        "অর্থনীতি",
        "technology innovation"
    ]
    
    print("\n" + "="*80)
    print("BM25 RETRIEVAL SYSTEM - TEST")
    print("="*80)
    
    for query in test_queries:
        results = retriever.search(query, top_k=5)
        retriever.print_results(results)
        input("Press Enter to continue to next query...")


if __name__ == "__main__":
    main()
