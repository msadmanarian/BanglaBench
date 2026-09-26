# Adjudication Protocol & Dispute Resolution
# Project: BanglaFactBench

---

## 1. Role of the Lead Adjudicator

The Lead Adjudicator is a senior researcher with formal background in Natural Language Processing and fact-checking methodology. The adjudicator's responsibility is to review all instances where Annotator 1 and Annotator 2 assigned conflicting veracity labels and assign the definitive `adjudicated_label`.

---

## 2. Structured Adjudication Workflow

```text
               [Conflicting Annotations: A1 ≠ A2]
                                │
                                ▼
         [Step 1: Evidence Inspection & Primary Source Check]
                                │
                                ▼
      [Step 2: Boundary Taxonomy Assessment (Guidelines Rulebook)]
                                │
                                ▼
   [Step 3: Adjudication Decision & Justification Rationale Record]
                                │
                                ▼
               [Step 4: Final Label Assignment]
```

### Dispute Resolution Rules:

1. **`REFUTED` vs. `MISLEADING`**:
   - Check if any component of the claim corresponds to a verifiable historical fact.
   - If genuine facts were deceptively re-contextualized, assign `MISLEADING`.
   - If the factual core is fabricated (e.g., event never happened, person never spoke), assign `REFUTED`.

2. **`SUPPORTED` vs. `MISLEADING`**:
   - Check if the claim omits crucial caveats that substantially change the public interpretation.
   - If omitted context is immaterial to the core assertion, assign `SUPPORTED`.
   - If omitted context directly contradicts the impression given by the headline, assign `MISLEADING`.

3. **`UNVERIFIABLE` vs. `REFUTED`**:
   - Check whether the lack of evidence is due to limited search or genuine epistemic absence.
   - If an authoritative entity (e.g., government ministry, verified police report) explicitly investigated and denied the event, assign `REFUTED`.
   - If no credible investigation or empirical data exists anywhere in public records, assign `UNVERIFIABLE`.

4. **`OPINION` vs. Empirical Labels**:
   - Check whether the claim contains an objective, verifiable predicate.
   - "অমুক দল সবচেয়ে দুর্নীতিগ্রস্ত" $\rightarrow$ Evaluative adjective without agreed objective criteria $\rightarrow$ `OPINION`.
   - "অমুক দলের সাধারণ সম্পাদক দুর্নীতি মামলায় দণ্ডিত হয়েছেন" $\rightarrow$ Empirical legal fact $\rightarrow$ `SUPPORTED` or `REFUTED` depending on court verdict.

---

## 3. Transparency & Disagreement Archiving

Every adjudicated claim preserves the original independent choices (`annotator_1` and `annotator_2`) alongside the final `adjudicated_label` and `annotation_notes`. This enables fine-grained disagreement analysis and allows researchers to evaluate model calibration on inherently difficult or borderline cases.
