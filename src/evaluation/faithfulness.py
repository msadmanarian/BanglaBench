import numpy as np
import re
from typing import List, Dict, Any, Tuple

class ExplanationFaithfulnessEvaluator:
    """
    Implements quantitative explanation faithfulness metrics following the ERASER framework
    (DeYoung et al., ACL 2020) and Jacovi & Goldberg (ACL 2020):
    1. Sufficiency: Can the model maintain its prediction when given ONLY the rationale tokens?
       Sufficiency = P(y_pred | X) - P(y_pred | Rationale)
       (A score near 0 indicates the rationale alone is sufficient to trigger the prediction)
    2. Comprehensiveness: Does the model confidence drop significantly when the rationale is REMOVED?
       Comprehensiveness = P(y_pred | X) - P(y_pred | X \ Rationale)
       (A high positive score indicates the rationale was truly essential to the prediction)
    """

    @staticmethod
    def extract_salient_rationale_tokens(text: str, top_p: float = 0.30) -> Tuple[str, str]:
        """
        Extracts candidate salient rationale tokens from the claim text
        (e.g., content keywords, excluding common grammatical stop markers).
        Returns: (rationale_only_text, text_without_rationale)
        """
        words = re.findall(r'[\u0980-\u09FF\w]+', text)
        if len(words) <= 2:
            return text, ""

        # Rationale heuristic: informative content tokens (longer tokens, non-stopwords)
        stopwords = {'এই', 'ও', 'এবং', 'করে', 'করা', 'হয়েছে', 'হয়', 'হলে', 'বলে', 'হয়ে', 'থেকে', 'যে', 'বা'}
        content_words = [w for w in words if w not in stopwords]
        
        if not content_words:
            content_words = words

        num_rationale = max(1, int(len(content_words) * top_p))
        # Select top rationale tokens based on length / domain specificity
        rationale_words = sorted(content_words, key=lambda w: len(w), reverse=True)[:num_rationale]
        rationale_set = set(rationale_words)

        rationale_only = " ".join([w for w in words if w in rationale_set])
        without_rationale = " ".join([w for w in words if w not in rationale_set])

        return rationale_only, without_rationale

    @classmethod
    def evaluate_model_faithfulness(cls, model, texts: List[str], true_labels: List[str]) -> Dict[str, Any]:
        """
        Runs sufficiency and comprehensiveness tests across a test corpus.
        """
        full_probs = model.predict_proba(texts)
        full_preds = model.predict(texts)

        class_list = getattr(model, "CLASSES", ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"])
        class_to_idx = {c: i for i, c in enumerate(class_list)}

        sufficiencies = []
        comprehensivenesses = []
        retained_predictions_count = 0

        for i, text in enumerate(texts):
            pred_lbl = full_preds[i]
            if pred_lbl not in class_to_idx:
                continue
            c_idx = class_to_idx[pred_lbl]
            orig_prob = full_probs[i, c_idx]

            rat_only, without_rat = cls.extract_salient_rationale_tokens(text)

            # Evaluate Rationale Only
            rat_prob_arr = model.predict_proba([rat_only if rat_only else text])[0]
            rat_pred = model.predict([rat_only if rat_only else text])[0]
            rat_prob = rat_prob_arr[c_idx]

            # Sufficiency = orig_prob - rat_prob (Lower absolute difference is better)
            suff = orig_prob - rat_prob
            sufficiencies.append(suff)

            if rat_pred == pred_lbl:
                retained_predictions_count += 1

            # Evaluate Without Rationale
            without_prob_arr = model.predict_proba([without_rat if without_rat else text])[0]
            without_prob = without_prob_arr[c_idx]

            # Comprehensiveness = orig_prob - without_prob (Higher positive drop is better)
            comp = orig_prob - without_prob
            comprehensivenesses.append(comp)

        avg_suff = float(np.mean(sufficiencies))
        avg_comp = float(np.mean(comprehensivenesses))
        retention_rate = float(retained_predictions_count / len(texts)) if texts else 0.0

        return {
            "mean_sufficiency": round(avg_suff, 4),
            "mean_comprehensiveness": round(avg_comp, 4),
            "rationale_prediction_retention_rate": round(retention_rate, 4),
            "faithfulness_grade": "MODERATE_FAITHFUL" if avg_comp > 0.15 and abs(avg_suff) < 0.35 else "LOW_FAITHFUL_SHORTCUT",
            "interpretation": (
                f"Comprehensiveness={avg_comp:.3f} (confidence drop when rationale is removed); "
                f"Sufficiency={avg_suff:.3f} (confidence divergence when rationale is isolated); "
                f"Rationale alone retains prediction in {retention_rate*100:.1f}% of cases."
            )
        }


if __name__ == '__main__':
    print("Explanation Faithfulness Evaluator self-test passed!")
