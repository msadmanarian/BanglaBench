"""
BanglaFactBench Controlled LLM Verification Module
Implements zero-shot, few-shot, and chain-of-verification prompting templates
for auditable, evidence-grounded claim evaluation without hidden chain-of-thought.
"""

import json
from typing import Dict, List, Any, Optional

class LLMClaimEvaluator:
    """
    Controlled prompt manager and evaluator for LLM-based Bengali claim verification.
    Follows Section 21 of the research specification.
    """

    SYSTEM_PROMPT_BN = (
        "আপনি একজন নিরপেক্ষ এবং নির্ভরযোগ্য বাংলা তথ্য যাচাইকারী (Fact-Checker)। "
        "আপনার কাজ হলো প্রদত্ত দাবিটি বিশ্লেষণ করা এবং যাচাইকৃত প্রমাণের ভিত্তিতে একটি সুনির্দিষ্ট সিদ্ধান্তে পৌঁছানো। "
        "কখনই ভিত্তিহীন তথ্য বা মনগড়া প্রমাণ ব্যবহার করবেন না। আপনার উত্তরটি অবশ্যই নির্ধারিত JSON ফরম্যাটে হতে হবে।"
    )

    LABELS = ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"]

    @classmethod
    def generate_zero_shot_prompt(cls, claim_text: str) -> str:
        prompt = f"""{cls.SYSTEM_PROMPT_BN}

যাচাই করার দাবি:
"{claim_text}"

সম্ভাব্য ক্যাটাগরি:
1. SUPPORTED: দাবিটি প্রত্যক্ষ প্রমাণের দ্বারা প্রমাণিত সত্য।
2. REFUTED: দাবিটি মিথ্যা, ভিত্তিহীন বা ভুল প্রমাণিত।
3. UNVERIFIABLE: দাবিটি নিশ্চিত বা অস্বীকার করার মতো পর্যাপ্ত তথ্য নেই।
4. MISLEADING: দাবিতে সত্যের কিছু উপাদান থাকলেও বিভ্রান্তিকরভাবে উপস্থাপন করা হয়েছে।
5. OPINION: বক্তব্যটি কোনো প্রমাণযোগ্য তথ্য নয়, বরং ব্যক্তিগত মতামত বা দৃষ্টিভঙ্গি।

অনুগ্রহ করে নিচের JSON ফরম্যাটে উত্তর দিন:
{{
  "claim": "{claim_text}",
  "verdict": "<SUPPORTED / REFUTED / UNVERIFIABLE / MISLEADING / OPINION>",
  "confidence": <0.0 থেকে 1.0 এর মধ্যে সংখ্যা>,
  "reasoning_bengali": "<সংক্ষিপ্ত ২-৩ লাইনের যৌক্তিক ব্যাখ্যা>",
  "verifiable_keywords": ["<মূল শব্দ ১>", "<মূল শব্দ ২>"]
}}
"""
        return prompt.strip()

    @classmethod
    def generate_few_shot_prompt(cls, claim_text: str, exemplar_claims: List[Dict]) -> str:
        exemplar_str = ""
        for i, ex in enumerate(exemplar_claims[:3], 1):
            exemplar_str += f"""
উদাহরণ {i}:
দাবি: "{ex['claim_text_normalized']}"
সিদ্ধান্ত: {ex['adjudicated_label']}
প্রমাণ লিংক: {ex.get('evidence_urls', [''])[0]}
"""

        prompt = f"""{cls.SYSTEM_PROMPT_BN}

নিচের কয়েকটি যাচাইকৃত উদাহরণ লক্ষ্য করুন:
{exemplar_str}

এখন নিচের নতুন দাবিটি যাচাই করুন:
দাবি: "{claim_text}"

নির্ধারিত JSON ফরম্যাটে উত্তর দিন:
{{
  "claim": "{claim_text}",
  "verdict": "<SUPPORTED / REFUTED / UNVERIFIABLE / MISLEADING / OPINION>",
  "confidence": <0.0 থেকে 1.0>,
  "reasoning_bengali": "<যৌক্তিক ব্যাখ্যা>",
  "cited_sources": ["<অনুমোদিত নির্ভরযোগ্য উৎস>"]
}}
"""
        return prompt.strip()

    @classmethod
    def parse_llm_response(cls, response_text: str) -> Dict[str, Any]:
        """
        Safely parses and validates JSON output from an LLM response.
        """
        try:
            # Extract JSON block if surrounded by markdown code fences
            clean_text = response_text.strip()
            if "```json" in clean_text:
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_text:
                clean_text = clean_text.split("```")[1].split("```")[0].strip()

            parsed = json.loads(clean_text)
            verdict = parsed.get("verdict", "").upper()
            if verdict not in cls.LABELS:
                verdict = "UNVERIFIABLE"
            parsed["verdict"] = verdict
            parsed["confidence"] = float(parsed.get("confidence", 0.5))
            return parsed
        except Exception as e:
            return {
                "error": f"Failed to parse LLM response: {str(e)}",
                "raw_text": response_text,
                "verdict": "UNVERIFIABLE",
                "confidence": 0.20
            }
