# AI Ethics, Data Integrity, and Responsible NLP
## Context Derived from AIUB Engineering Ethics & OBE Guidelines

This document synthesizes the ethical principles and compliance frameworks drawn from the AIUB Engineering Ethics course (`G:\AIUB\26 - 2 - Semester 9\Ethics`).

---

## 1. Ethical Imperatives in Automated Fact-Checking

Automated claim verification directly intersects with public trust, freedom of speech, political neutrality, and health safety. According to the AIUB Engineering Ethics syllabus (grounded in ACM Code of Ethics Section 1.2 "Avoid Harm" and IEEE Code of Ethics Section 1 "Hold paramount the safety, health, and welfare of the public"):

1. **Avoidance of Algorithmic Censorship**: Automated classifiers must never be deployed as unilateral arbiters of truth without human oversight. Classifiers make statistical errors; treating model predictions as objective truth can suppress legitimate democratic discourse or amplify false consensus.
2. **Harm Mitigation in High-Stakes Domains**:
   - **Public Health**: Misclassifying a medical warning or false cure can cause physical injury or death.
   - **Disaster & Emergencies**: Spreading unverified rescue instructions or mislabeling verified relief announcements can disrupt humanitarian response.
   - **Finance**: Unverified market claims can trigger economic fraud or panic.
3. **Data Privacy & Personally Identifiable Information (PII)**:
   - Claims must strictly focus on verifiable propositions of public interest.
   - Private citizen identifiers (phone numbers, private addresses, personal photos) must be redacted or excluded.
   - Public figures (politicians, government officials, corporate spokespersons) are documented only in their public, official capacity.

---

## 2. Anti-Fabrication & Scientific Honesty

In alignment with IEEE Code of Ethics item 3 ("be honest and realistic in stating claims or estimates based on available data") and AIUB academic integrity regulations:
- **Zero Fabrication Policy**: No paper, citation, author, DOI, URL, benchmark number, accuracy score, F1 score, or Cohen's kappa statistic may ever be manufactured or guessed.
- **Unverified Status Marker**: If an empirical value or citation cannot be independently confirmed, it must be designated `UNVERIFIED` and excluded from evidentiary conclusions.
- **Transparent Failure Reporting**: Unfavorable results, model collapses under adversarial perturbations, and poor cross-domain transfer must be reported with equal prominence as successful results.
