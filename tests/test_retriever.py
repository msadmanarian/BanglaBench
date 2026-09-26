import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'retrieval'))
from bm25_retriever import BM25Retriever

def test_bm25_index_and_retrieve():
    corpus = [
        "ডেঙ্গু জ্বরে পেঁপে পাতার রস কোনো বৈজ্ঞানিক নিরাময় নয়।",
        "বাংলাদেশ ব্যাংক বৈদেশিক মুদ্রার রিজার্ভ প্রকাশ করেছে।",
        "পদ্মা সেতু সম্পূর্ণ বাংলাদেশ সরকারের অর্থায়নে নির্মিত।"
    ]
    meta = [{"id": "doc1"}, {"id": "doc2"}, {"id": "doc3"}]
    retriever = BM25Retriever()
    retriever.index(corpus, metadata=meta)

    # Query for dengue
    results = retriever.retrieve("ডেঙ্গু রোগীর চিকিৎসা এবং পেঁপে পাতা", top_k=1)
    assert len(results) == 1
    assert results[0]["metadata"]["id"] == "doc1"
    assert results[0]["score"] > 0

def test_empty_query_handling():
    corpus = ["নমুনা প্রমাণ বাক্য।"]
    retriever = BM25Retriever()
    retriever.index(corpus)
    results = retriever.retrieve("", top_k=3)
    assert len(results) == 0
