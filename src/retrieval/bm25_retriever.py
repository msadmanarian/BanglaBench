import math
import re
from typing import List, Dict, Tuple

class BM25Retriever:
    """
    Native implementation of Okapi BM25 for Bengali claim evidence retrieval.
    Follows Robertson & Zaragoza (2009).
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avg_doc_len = 0.0
        self.doc_freqs = {}
        self.idf = {}
        self.doc_lens = []
        self.docs = []
        self.metadata = []

    @staticmethod
    def tokenize(text: str) -> List[str]:
        # Tokenize by Bengali and Latin alphanumeric tokens
        return re.findall(r'[\u0980-\u09FF\w]+', text.lower())

    def index(self, documents: List[str], metadata: List[Dict] = None):
        """
        Indexes a list of textual passages / evidence documents.
        """
        self.docs = documents
        self.metadata = metadata if metadata else [{} for _ in documents]
        self.corpus_size = len(documents)
        
        tokenized_docs = [self.tokenize(doc) for doc in documents]
        self.doc_lens = [len(doc) for doc in tokenized_docs]
        self.avg_doc_len = sum(self.doc_lens) / self.corpus_size if self.corpus_size > 0 else 0.0

        # Compute document frequencies
        self.doc_freqs = {}
        for doc in tokenized_docs:
            seen = set(doc)
            for word in seen:
                self.doc_freqs[word] = self.doc_freqs.get(word, 0) + 1

        # Compute Robertson-Spärck Jones IDF
        self.idf = {}
        for word, freq in self.doc_freqs.items():
            # Standard BM25 IDF formulation with floor smoothing
            idf_val = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)
            self.idf[word] = max(idf_val, 0.01)

        self.tokenized_docs = tokenized_docs
        return self

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Scores all indexed documents against query and returns top_k results.
        """
        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []
        scores = [0.0] * self.corpus_size

        for q in query_tokens:
            if q not in self.idf:
                continue
            q_idf = self.idf[q]

            for i, doc in enumerate(self.tokenized_docs):
                doc_len = self.doc_lens[i]
                freq = doc.count(q)
                if freq == 0:
                    continue

                num = freq * (self.k1 + 1.0)
                denom = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                scores[i] += q_idf * (num / denom)

        # Rank documents
        ranked_indices = sorted(range(self.corpus_size), key=lambda idx: scores[idx], reverse=True)
        results = []
        for idx in ranked_indices[:top_k]:
            if scores[idx] > 0.0 or len(results) == 0:
                results.append({
                    "doc_index": idx,
                    "score": round(float(scores[idx]), 4),
                    "document_text": self.docs[idx],
                    "metadata": self.metadata[idx]
                })

        return results


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    retriever = BM25Retriever()
    corpus = [
        "স্বাস্থ্য অধিদপ্তর জানিয়েছে পেঁপে পাতার রসে ডেঙ্গু নিরাময়ের বৈজ্ঞানিক ভিত্তি নেই।",
        "পদ্মা সেতু বাংলাদেশের নিজস্ব অর্থায়নে নির্মিত হয়েছে এবং এটি দেশের অর্থনীতিতে অবদান রাখছে।",
        "ইপিআই কর্মসূচির মাধ্যমে শিশুদের ১০টি মারাত্মক রোগের টিকা সম্পূর্ণ বিনামূল্যে দেওয়া হয়।"
    ]
    meta = [
        {"source": "DGHS", "url": "https://dghs.gov.bd"},
        {"source": "Cabinet", "url": "https://cabinet.gov.bd"},
        {"source": "EPI", "url": "https://dghs.gov.bd/epi"}
    ]
    retriever.index(corpus, meta)
    res = retriever.retrieve("ডেঙ্গু রোগীর জন্য পেঁপে পাতা", top_k=2)
    print("Query: ডেঙ্গু রোগীর জন্য পেঁপে পাতা")
    for r in res:
        print(f"Score: {r['score']} | Doc: {r['document_text']}")
    assert res[0]["doc_index"] == 0
    print("BM25 self-test passed!")
