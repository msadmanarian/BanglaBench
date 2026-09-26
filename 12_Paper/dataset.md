# 3. The BanglaFactBench Dataset

### 3.1 Corpus Collection and Scope
BanglaFactBench was constructed to represent the diverse linguistic and informational ecosystem of Bengali public discourse. Data was systematically sampled from legitimate, publicly verifiable sources:
1. **Fact-Checking Portals**: Rumor Scanner Bangladesh (IFCN signatory), FactWatch (University of Liberal Arts Bangladesh), and Boom Bangladesh.
2. **Authoritative News Media**: Prothom Alo, The Daily Star (Bangla), and BBC News Bangla.
3. **Official Governmental & Institutional Portals**: Bangladesh Bank, Ministry of Health and Family Welfare (MOHFW), Directorate General of Drug Administration (DGDA), and SPARSO.
4. **Public Social Media Feeds**: Monitored viral public rumors on Facebook and YouTube.

The dataset spans six primary domains:
- **Politics**: Electoral integrity, political appointments, international treaties.
- **Public Health**: Dengue cures, pharmaceutical bans, vaccine safety, communicable disease statistics.
- **Finance & Economy**: Bangladesh Bank foreign exchange reserves, currency demonetization, loan defaults.
- **Disaster Management**: Cyclone landfall forecasts, flood relief distributions, earthquake damage reports.
- **Science & Technology**: Space exploration (SPARSO), telecommunications (5G rollouts), artificial intelligence.
- **Social Issues & Infrastructure**: Padma bridge financing, metro rail protocols, university admissions.

### 3.2 Taxonomic Schema
Rather than a simple binary flag (`true`/`false`), we employ an expressive 5-class schema:
1. `SUPPORTED`: The claim is directly substantiated by authoritative evidence.
2. `REFUTED`: The claim is directly contradicted by factual evidence or debunked by accredited fact-checkers.
3. `UNVERIFIABLE`: Current publicly available evidence is insufficient to confirm or deny the claim.
4. `MISLEADING`: The claim combines elements of truth with manipulated context, deceptive framing, or omitted details.
5. `OPINION`: The statement reflects subjective value judgments, moral beliefs, or political commentary devoid of falsifiable factual propositions.

### 3.3 Dual Independent Annotation & Agreement
Annotation was conducted following formal guidelines (`annotation_guidelines.md`). Each claim was independently evaluated by two trained bilingual annotators who inspected the claim text, retrieved external corroborating URLs, and assigned a label and confidence score.

Empirical agreement was computed using Cohen's kappa ($\kappa$):
- Total Claims Annotated: $N = 60$
- Observed Agreement: $P_o = \frac{56}{60} = 93.33\%$
- Chance Agreement: $P_e = 24.22\%$
- **Cohen's Kappa ($\kappa$)**: **0.9120** (Denoting "Almost Perfect Agreement" under Landis & Koch, 1977).

All 4 disagreement cases (predominantly between `REFUTED` and `MISLEADING`) were resolved through structured adjudication (`adjudication_protocol.md`) led by a senior adjudicator with formal notes recorded in the corpus metadata.

### 3.4 Data Normalization and Preprocessing
All claim texts were processed through our deterministic normalization pipeline (`normalizer.py`):
1. **Unicode NFC Standardization**: Eliminating duplicate Unicode representations of Bengali conjuncts and vowel modifiers.
2. **Punctuation & Dari Harmonization**: Standardizing traditional Bengali dari (`।`) and European punctuation.
3. **Deduplication Audit**: String-level and character 3-gram Jaccard audits verified that near-duplicate and duplicate pairs were completely removed.
