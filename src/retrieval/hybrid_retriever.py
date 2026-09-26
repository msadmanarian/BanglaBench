"""
BanglaFactBench Hybrid Dense-Sparse Evidence Retriever
Combines sparse Okapi BM25 matching with subword character n-gram cosine similarity
to resolve vocabulary mismatch when claims are subjected to paraphrasing.
"""

import math
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from bm25_retriever import BM25Retriever

class HybridEvidenceRetriever:
    """
    Hybrid retriever interpolating BM25 and Character TF-IDF cosine similarity.
    Score = alpha * BM25_norm + (1 - alpha) * Dense_norm
    """

    def __init__(self, alpha: float = 0.5, k1: float = 1.5, b: float = 0.75):
        self.alpha = alpha
        self.bm25 = BM25Retriever(k1=k1, b=b)
        self.vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        self.tfidf_matrix = None
        self.docs = []
        self.metadata = []

    def index(self, documents: List[str], metadata: List[Dict] = None):
        self.docs = documents
        self.metadata = metadata if metadata else [{} for _ in documents]
        self.bm25.index(documents, metadata)
        if len(documents) > 0:
            self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        return self

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not query or not query.strip():
            return []

        # 1. Sparse BM25 scores
        bm25_res = self.bm25.retrieve(query, top_k=len(self.docs))
        bm25_score_map = {r["doc_index"]: r["score"] for r in bm25_res}
        max_bm25 = max(bm25_score_map.values()) if bm25_score_map and max(bm25_score_map.values()) > 0 else 1.0

        # 2. Dense Character n-gram cosine similarity
        q_vec = self.vectorizer.transform([query])
        cos_sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        # 3. Hybrid fusion
        fused = []
        for idx in range(len(self.docs)):
            s_bm25 = bm25_score_map.get(idx, 0.0) / max_bm25
            s_dense = float(cos_sims[idx])
            hybrid_score = self.alpha * s_bm25 + (1.0 - self.alpha) * s_dense
            fused.append((idx, hybrid_score, self.docs[idx], self.metadata[idx]))

        fused.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score, doc_text, meta in fused[:top_k]:
            results.append({
                "doc_index": idx,
                "score": round(float(score), 4),
                "document_text": doc_text,
                "metadata": meta
            })
        return results
