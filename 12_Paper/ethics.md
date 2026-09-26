# 8. Ethical Considerations

### 8.1 Dual-Use and Misinformation Amplification
Research into misinformation detection inherently touches upon sensitive, potentially harmful real-world claims. To mitigate the risk of amplifying false narratives or causing panic:
- We do not generate synthetic, toxic, or slanderous political disinformation.
- All perturbed claims in the adversarial suite (Split E) are constructed strictly to preserve the semantic intent of already published rumors for evaluation purposes, rather than to manufacture novel falsehoods.
- Public documentation provides full factual debunks and authoritative evidence URLs for all analyzed claims.

### 8.2 Privacy and Personally Identifiable Information (PII)
All claims included in BanglaFactBench were sourced from publicly accessible news publications, accredited fact-checking agencies, or public government announcements. We strictly excluded private personal correspondences, private WhatsApp groups, and individual private citizens. Where public figures (e.g., political leaders, ministers) are referenced, they are evaluated exclusively in the context of their public official duties.

### 8.3 Political Neutrality
Fact-checking research in polarized environments risks accusations of partisan bias. We ensured political neutrality by:
1. Sampling claims from diverse media perspectives across both state-affiliated and independent outlets.
2. Grounding all political verifications strictly in constitutional documents, parliamentary records, and audited election observer reports.
3. Explicitly decoupling fact-checking (`REFUTED`/`SUPPORTED`) from political opinion (`OPINION`).

### 8.4 Public Health and Medical Disclaimers
Public health claims (concerning dengue fever, vaccines, and pharmaceutical bans) are verified strictly against authoritative health bodies, including the Directorate General of Drug Administration (DGDA), the World Health Organization (WHO), and peer-reviewed clinical studies. Benchmark predictions must never be used as clinical diagnostic or treatment advice without physician consultation.
