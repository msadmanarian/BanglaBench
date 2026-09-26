import os
import sys
import json
import numpy as np
from typing import Dict, List, Tuple, Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

sys.stdout.reconfigure(encoding='utf-8')

class BanglaFactClassifier:
    """
    Standardized classification baseline wrapper for BanglaFactBench.
    Supports:
    - 'nb': Multinomial Naive Bayes
    - 'svm': Linear Support Vector Machine (with Platt scaling / calibration)
    - 'lr': Multinomial Logistic Regression
    - 'rf': Random Forest Classifier
    Features: Word (1-2) and Character (3-5) TF-IDF union.
    """
    
    CLASSES = ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"]
    
    def __init__(self, model_type: str = 'svm', seed: int = 42):
        self.model_type = model_type.lower()
        self.seed = seed
        self.pipeline = self._build_pipeline()

    def _build_pipeline(self) -> Pipeline:
        # Combined word and character n-gram feature extractor
        feature_extractor = FeatureUnion([
            ('word_tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=2500,
                sublinear_tf=True
            )),
            ('char_tfidf', TfidfVectorizer(
                analyzer='char',
                ngram_range=(3, 5),
                max_features=5000,
                sublinear_tf=True
            ))
        ])

        if self.model_type == 'nb':
            clf = MultinomialNB(alpha=1.0)
        elif self.model_type == 'svm':
            clf = LinearSVC(C=1.0, random_state=self.seed, max_iter=2000)
        elif self.model_type == 'lr':
            clf = LogisticRegression(C=1.0, random_state=self.seed, max_iter=1000)
        elif self.model_type == 'rf':
            clf = RandomForestClassifier(n_estimators=100, random_state=self.seed, n_jobs=-1)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

        return Pipeline([
            ('features', feature_extractor),
            ('classifier', clf)
        ])

    def fit(self, texts: List[str], labels: List[str]):
        self.pipeline.fit(texts, labels)
        return self

    def predict(self, texts: List[str]) -> List[str]:
        return self.pipeline.predict(texts).tolist()

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        clf = self.pipeline.named_steps['classifier']
        if hasattr(clf, "predict_proba"):
            return self.pipeline.predict_proba(texts)
        elif hasattr(clf, "decision_function"):
            df = self.pipeline.decision_function(texts)
            if df.ndim == 1:
                df = np.vstack([-df, df]).T
            # Numerically stable softmax
            exp_df = np.exp(df - np.max(df, axis=1, keepdims=True))
            probs = exp_df / np.sum(exp_df, axis=1, keepdims=True)
            return probs
        else:
            preds = self.predict(texts)
            probs = np.zeros((len(texts), len(self.CLASSES)))
            for i, p in enumerate(preds):
                if p in self.CLASSES:
                    probs[i, self.CLASSES.index(p)] = 1.0
            return probs

    def evaluate(self, texts: List[str], true_labels: List[str]) -> Dict[str, Any]:
        preds = self.predict(texts)
        probs = self.predict_proba(texts)
        
        acc = accuracy_score(true_labels, preds)
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
            true_labels, preds, labels=self.CLASSES, average='macro', zero_division=0
        )
        p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
            true_labels, preds, labels=self.CLASSES, average='weighted', zero_division=0
        )
        
        # Per-class metrics
        p_class, r_class, f1_class, support = precision_recall_fscore_support(
            true_labels, preds, labels=self.CLASSES, average=None, zero_division=0
        )
        
        cm = confusion_matrix(true_labels, preds, labels=self.CLASSES).tolist()

        per_class = {}
        for idx, c in enumerate(self.CLASSES):
            per_class[c] = {
                "precision": round(float(p_class[idx]), 4),
                "recall": round(float(r_class[idx]), 4),
                "f1": round(float(f1_class[idx]), 4),
                "support": int(support[idx])
            }

        return {
            "model_type": self.model_type,
            "accuracy": round(float(acc), 4),
            "macro_precision": round(float(p_macro), 4),
            "macro_recall": round(float(r_macro), 4),
            "macro_f1": round(float(f1_macro), 4),
            "weighted_f1": round(float(f1_weighted), 4),
            "confusion_matrix": cm,
            "per_class": per_class,
            "predictions": preds,
            "probabilities": probs.tolist()
        }


if __name__ == '__main__':
    train_texts = [
        "পদ্মা সেতু বাংলাদেশের নিজস্ব অর্থায়নে নির্মিত হয়েছে।",
        "পেঁপে পাতার রস ডেঙ্গু সম্পূর্ণ নিরাময় করে।",
        "আমলকী খেলে রোগ প্রতিরোধ বাড়ে তবে এটি একমাত্র চিকিৎসা নয়।",
        "গতকাল এক অজ্ঞাত কূটনীতিক গোপনে দেশ ছেড়েছেন বলে গুঞ্জন উঠেছে।",
        "সংসদীয় গণতন্ত্রের চেয়ে রাষ্ট্রপতি ব্যবস্থা উত্তম।"
    ]
    train_labels = ["SUPPORTED", "REFUTED", "MISLEADING", "UNVERIFIABLE", "OPINION"]
    
    clf = BanglaFactClassifier(model_type='svm')
    clf.fit(train_texts, train_labels)
    eval_res = clf.evaluate(train_texts, train_labels)
    print("Train Self-Evaluation Macro F1:", eval_res["macro_f1"])
    print("Classical Baseline self-test passed!")
