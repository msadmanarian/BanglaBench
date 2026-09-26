# Decision Log: BanglaFactBench

This log records every key methodological, architectural, and experimental decision made during the project, along with alternatives considered, justification, evidence, and consequences.

---

### Decision D-001: Separation of Research Workspace from Original AIUB Files
- **Decision**: Keep all original files in `G:\AIUB` completely read-only and unaltered. Conduct all research, dataset construction, experimentation, and paper writing in `g:\Events\BanglaBench`.
- **Alternatives Considered**: Modifying or creating folders directly inside `G:\AIUB\26 - 2 - Semester 9\`.
- **Reason**: Preserves the integrity of academic coursework archives and prevents file contamination or accidental deletion.
- **Evidence**: Master Prompt Guideline Section 3 ("The original university files must remain unchanged. Create a separate research workspace.").
- **Consequence**: Workspace is cleanly containerized in `g:\Events\BanglaBench`, easily version-controlled with Git, and reproducible on external machines.

---

### Decision D-002: Claim-Level Unit of Analysis over Article-Level Classification
- **Decision**: Define the primary unit of evaluation as an individual atomic **CLAIM** rather than an entire full-length article.
- **Alternatives Considered**: Document-level / news-article fake news classification (as seen in older datasets like BanFakeNews).
- **Reason**: Full-length news classification encourages models to learn superficial stylistic or topic-based shortcuts (e.g., sensationalist wording, author style, specific newspaper vocabulary) rather than verifying factual assertions against evidence. Claim-level verification tests true reasoning and allows fine-grained retrieval-augmented evidence grounding.
- **Evidence**: Thorne et al. (FEVER, 2018); Wadden et al. (SciFact, 2020); Gupta & Srikumar (X-Fact, 2021).
- **Consequence**: Dataset schema must capture atomic claims, context, source, and associated evidence URLs/text.

---

### Decision D-003: Five-Class Fine-Grained Fact-Checking Taxonomy
- **Decision**: Adopt a 5-class label taxonomy: `SUPPORTED`, `REFUTED`, `UNVERIFIABLE`, `MISLEADING`, `OPINION`.
- **Alternatives Considered**: Binary classification (`TRUE` vs. `FALSE`) or 3-class FEVER schema (`SUPPORTS`, `REFUTES`, `NOT ENOUGH INFO`).
- **Reason**: Binary and 3-class schemas fail to represent nuanced misinformation patterns prominent in the Bengali media ecosystem—specifically cherry-picked half-truths (`MISLEADING`) and value judgments masquerading as verifiable facts (`OPINION`).
- **Evidence**: PolitiFact truth-o-meter taxonomy; Snopes rating systems; Boom Bangladesh fact-checking methodology.
- **Consequence**: Annotation protocol must provide precise boundary definitions and borderline examples distinguishing between `UNVERIFIABLE`, `MISLEADING`, and `OPINION`.

---

### Decision D-004: Multi-Split Benchmark Evaluation (Splits A through E)
- **Decision**: Benchmark models across five distinct evaluation splits: Random Split (Split A), Cross-Domain Split (Split B), Cross-Source Split (Split C), Temporal Split (Split D), and Adversarial Perturbation Split (Split E).
- **Alternatives Considered**: Standard single 80/10/10 random stratified train/test split.
- **Reason**: A random split severely overestimates real-world model performance due to identical source distributions, shared events, and temporal leakage. A multi-split design rigorously assesses out-of-distribution generalization.
- **Evidence**: AIUB CSC 4232 OBE Evaluation Rigor (CO3); Ribeiro et al. (CheckList, 2020); Gorman & Bedrick (2019) on dataset split leakage.
- **Consequence**: Training and evaluation pipelines must support modular partition configurations.
