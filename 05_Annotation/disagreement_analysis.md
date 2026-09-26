# Disagreement Analysis & Adjudication Case Log
# Project: BanglaFactBench

---

## 1. Overview
Out of 60 claims annotated by two independent evaluators, exactly **4 claims (6.7%)** exhibited boundary disagreements. All cases were resolved via the formal Adjudication Protocol (`adjudication_protocol.md`).

---

## 2. Itemized Disagreement Case Log

| Claim ID | Claim Text | Annotator 1 | Annotator 2 | Adjudicated | Reason for Resolution |
|---|---|:---:|:---:|:---:|---|
| `BFB-HLT-0004` | আমলকী খেলে শরীরের রোগ প্রতিরোধ ক্ষমতা বহুগুণ বাড়ে, তাই এটি যেকোনো সংক্রামক রোগ প্রতিরোধে এককভাবে যথেষ্ট। | `MISLEADING` | `REFUTED` | **`MISLEADING`** | আমলকীর পুষ্টিগুণের সত্য তথ্যকে ভিত্তি করে বিভ্রান্তিকর ও অতিমাত্রার উপসংহার টানা হয়েছে। |
| `BFB-HLT-0008` | ডায়াবেটিসে আক্রান্ত রোগীরা তিতা করলার রস নিয়মিত পান করলে চিরতরে ইনসুলিন গ্রহণ বন্ধ করতে পারেন। | `MISLEADING` | `REFUTED` | **`MISLEADING`** | খাবারের আংশিক উপকারিতাকে ফুল-কিউর বা ওষুধের বিকল্প দাবি করে বিপজ্জনক বিভ্রান্তি তৈরি। |
| `BFB-DIS-0003` | সিলেট অঞ্চলে সাম্প্রতিক বন্যার প্রধান কারণ হচ্ছে ভারতের গজলডোবা বাঁধের সব গেট হঠাৎ খুলে দেওয়া। | `REFUTED` | `MISLEADING` | **`REFUTED`** | ভৌগোলিক অববাহিকা সম্পূর্ণরূপে ভুল। তিস্তা অববাহিকার বাঁধ দিয়ে সুরমা-কুশিয়ারা অববাহিকার বন্যার ব্যাখ্যা দেওয়া সম্পূর্ণ ভ্রান্ত। |
| `BFB-SCI-0003` | স্মার্টফোন সারারাত চার্জে লাগিয়ে রাখলে ব্যাটারি অতিরিক্ত স্ফীত হয়ে নিশ্চিতভাবে বিস্ফোরণ ঘটবে। | `MISLEADING` | `REFUTED` | **`MISLEADING`** | ত্রুটিপূর্ণ ব্যাটারির সাধারণ ঝুঁকিকে আধুনিক স্মার্টফোনের অনিবার্য পরিণতি হিসেবে অতিরঞ্জিতভাবে উপস্থাপন করা হয়েছে। |

---

## 3. Methodological Insights for Guideline Refinement

1. **The `REFUTED` vs. `MISLEADING` Boundary**:
   - When a claim begins from an authentic medical or botanical fact (e.g., amla contains vitamin C, bitter gourd contains polypeptide-p) but asserts complete disease eradication without medicine, Annotator 1 leaned toward `MISLEADING` (recognizing the underlying true premise) while Annotator 2 selected `REFUTED` (recognizing the falsity of the medical conclusion).
   - *Adjudication Rule Enforced*: If the premise is true but the overarching claim asserts a clinically false causal relationship or medical cure, the classification is formalized as `MISLEADING` if partial truth exists, or `REFUTED` if the primary proposition is medically disproven.

2. **The `DISASTER` Regional Ambiguity**:
   - For flood claims mentioning specific barrages (e.g., Gajaldoba barrage in Sylhet flood rumors), one annotator viewed it as `MISLEADING` because Gajaldoba exists and releases water, while the adjudicator confirmed `REFUTED` because the Teesta basin is geographically disconnected from the Surma-Kushiyara basin.
