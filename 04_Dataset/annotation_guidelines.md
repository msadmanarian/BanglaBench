# Annotation Guidelines & Label Taxonomy
# Project: BanglaFactBench

---

## 1. Introduction and Guiding Principles

The objective of annotation in **BanglaFactBench** is to assign a standardized, defensible veracity label to atomic Bengali factual claims based strictly on authoritative, verifiable evidence.

### Cardinal Annotation Rules:
1. **Evidence-Grounded**: Do NOT label based on personal beliefs, political sympathies, or general world impressions. A claim can only be marked `SUPPORTED` or `REFUTED` if authoritative published evidence is documented.
2. **Atomic Proposition**: Focus on the core factual assertion of the claim, ignoring extraneous rhetorical flourishes.
3. **Temporal Awareness**: Judge the claim relative to the state of evidence at the recorded `claim_date`.
4. **Strict Distinction Between Fact and Opinion**: Subjective value judgments without empirical testability must be labeled `OPINION`.

---

## 2. 5-Class Label Taxonomy

```text
                                  [Input Claim]
                                        │
                    Is it an empirical factual proposition?
                                  /           \
                                NO             YES
                               /                 \
                          [OPINION]        Is there sufficient authoritative evidence?
                                                  /                 \
                                                 NO                  YES
                                                /                      \
                                        [UNVERIFIABLE]        Does the evidence match the claim?
                                                                 /         |         \
                                                          MATCHES   CONTRADICTS   DISTORTED
                                                            /              |            \
                                                     [SUPPORTED]      [REFUTED]    [MISLEADING]
```

---

### Label 1: `SUPPORTED`

- **Definition**: The claim makes an empirical factual assertion that is directly substantiated and confirmed by credible, authoritative evidence.
- **Inclusion Criteria**:
  - Authoritative sources (official statistical bulletins, gazettes, certified research studies, peer-reviewed medical journals, IFCN fact-check reports) explicitly verify the statement.
  - Key figures, dates, events, and entity relations stated in the claim are accurate within acceptable reporting margins.
- **Exclusion Criteria**:
  - The claim leaves out critical qualifiers that invert its meaning (classify as `MISLEADING`).
  - The claim is partly true but contains fabricated secondary elements (classify as `MISLEADING`).
- **Example**:
  - *Claim*: "পদ্মা সেতু বাংলাদেশের নিজস্ব অর্থায়নে নির্মিত হয়েছে।" (Padma Bridge was constructed using Bangladesh's own financing.)
  - *Evidence*: Official Ministry of Finance and Cabinet Division project closeout documents confirm domestic funding allocations.
  - *Verdict*: `SUPPORTED`
- **Borderline Case**: A claim reports a casualty number slightly rounded (e.g., "প্রায় ৫০ জন নিহত" when the official tally is 48). If standard qualifiers ("প্রায়" / approximately) are used, classify as `SUPPORTED`.

---

### Label 2: `REFUTED`

- **Definition**: The claim makes an empirical factual assertion that is directly contradicted, disproven, or exposed as fabricated by authoritative evidence.
- **Inclusion Criteria**:
  - The core premise is false: the event never occurred, the quoted statement was never made, the image/video was fabricated or completely unrelated, or scientific consensus refutes the assertion.
  - An authentic primary source explicitly disproves the assertion.
- **Exclusion Criteria**:
  - The claim is merely exaggerated or selectively framed without being outright false (classify as `MISLEADING`).
- **Example**:
  - *Claim*: "করোনা ভ্যাকসিনের মাধ্যমে মানুষের শরীরে মাইক্রোচিপ প্রবেশ করানো হচ্ছে।" (Microchips are being implanted into human bodies via COVID-19 vaccines.)
  - *Evidence*: World Health Organization (WHO) and biomedical clinical trial documentation verify vaccine biochemical compositions containing no electronic components.
  - *Verdict*: `REFUTED`
- **Borderline Case**: An authentic historical photo is presented, but with a completely fabricated caption claiming it depicts an event from yesterday. Because the core assertion ("this event happened yesterday") is completely contradicted by fact, classify as `REFUTED`.

---

### Label 3: `UNVERIFIABLE`

- **Definition**: The claim asserts a factual proposition, but available authoritative public sources are insufficient, absent, or fundamentally inconclusive at the time of verification.
- **Inclusion Criteria**:
  - Independent investigation finds no primary documents, credible journalistic reports, official records, or empirical data either confirming or disproving the claim.
  - Sources provide conflicting reports of equal credibility without resolution.
- **Exclusion Criteria**:
  - A claim is false, but the annotator merely failed to search properly. (Exhaustive search is required before assigning `UNVERIFIABLE`).
  - Subjective personal statements lacking testability (classify as `OPINION`).
- **Example**:
  - *Claim*: "গতকাল রাতে সুন্দরবনের গহীনে একটি নতুন প্রজাতির বাঘ দেখা গেছে বলে এক গ্রামবাসী দাবি করেছেন।" (A villager claimed to have seen a new species of tiger deep in the Sundarbans last night.)
  - *Evidence*: Forest Department has no record, no photograph or physical evidence exists, and the claim cannot be independently confirmed or disproven.
  - *Verdict*: `UNVERIFIABLE`

---

### Label 4: `MISLEADING`

- **Definition**: The claim contains elements of truth or accurate historical facts, but presents them with deceptive framing, altered context, omitted vital facts, or false causal connections that lead to a fundamentally false conclusion.
- **Inclusion Criteria**:
  - Cherry-picked data or statistics (e.g., citing inflation numbers from a single favorable week while ignoring annual trends).
  - Out-of-context genuine media (e.g., an authentic 2015 flood photo circulated during a 2024 political rally to claim government negligence).
  - Accurate premises combined with an unfounded, manipulative conclusion.
- **Exclusion Criteria**:
  - The claim is 100% fabricated without any genuine factual basis (classify as `REFUTED`).
- **Example**:
  - *Claim*: "বাংলাদেশে চালের দাম এক রাতেই ৫০% কমে গেছে।" (Rice prices in Bangladesh dropped by 50% overnight.)
  - *Evidence*: A single subsidized government fair-price truck sold rice at 50% discount to low-income ration-card holders, but general open market retail prices remained unchanged.
  - *Verdict*: `MISLEADING`
- **Borderline Case**: A politician quotes an authentic economic statistic from 5 years ago as if it reflects the current economy today. Because the number itself was real but the temporal framing is intentionally deceptive, classify as `MISLEADING`.

---

### Label 5: `OPINION`

- **Definition**: The claim expresses a subjective viewpoint, value judgment, belief, aesthetic preference, or speculative prediction that cannot be definitively tested as true or false against empirical factual records.
- **Inclusion Criteria**:
  - Statements containing evaluative adjectives without empirical benchmarks (e.g., "সেরা" / best, "সবচেয়ে সুন্দর" / most beautiful, "অযোগ্য" / incompetent).
  - Speculative predictions about unobservable future events (e.g., "আগামী বছর নির্বাচন না-ও হতে পারে").
  - Moral, philosophical, or religious belief statements.
- **Exclusion Criteria**:
  - A statement phrased as an opinion that contains a verifiable factual predicate (e.g., "আমার মতে অমুক মন্ত্রী ঘুষ খেয়েছেন" contains an actionable factual claim of bribery).
- **Example**:
  - *Claim*: "বাংলাদেশ ক্রিকেট দলের বর্তমান অধিনায়ক দেশের ইতিহাসের সবচেয়ে দূরদর্শী নেতা।" (The current captain of the Bangladesh cricket team is the most visionary leader in the country's history.)
  - *Evidence*: "Visionary" is an inherently subjective appraisal without objective consensus criteria.
  - *Verdict*: `OPINION`

---

## 3. Disagreement Resolution & Adjudication Protocol

When Annotator 1 and Annotator 2 assign differing labels:
1. If the disagreement is between `REFUTED` and `MISLEADING`, both annotators re-examine whether any factual element in the claim was authentic. If authentic elements were distorted, consensus defaults to `MISLEADING`; if the core premise is entirely fabricated, consensus defaults to `REFUTED`.
2. If consensus cannot be reached, the Senior Adjudicator reviews the primary evidence and issues a binding `adjudicated_label` with documented rationale.
