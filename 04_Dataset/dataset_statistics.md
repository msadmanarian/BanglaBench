# Dataset Statistics: BanglaFactBench
# Programmatically Calculated on 60 Curated Core Claims

This report presents descriptive statistics calculated programmatically from the gold-standard annotated benchmark `04_Dataset/annotated/claims_annotated.json`.

---

## 1. Overall Summary

| Metric | Statistic |
|---|---|
| **Total Core Claims** | **60** |
| **Topical Domains** | **6** (`politics`, `health`, `finance`, `disaster`, `sci_tech`, `social`) |
| **Veracity Labels** | **5** (`SUPPORTED`, `REFUTED`, `UNVERIFIABLE`, `MISLEADING`, `OPINION`) |
| **Evidence Grounding Rate** | **100.0%** (60/60 claims with authoritative URLs) |
| **Average Claim Word Count** | **15.0 words** (Range: 10 to 22 words) |
| **Average Character Length** | **104.2 characters** |
| **Inter-Annotator Agreement (Cohen's $\\kappa$)** | **0.9120** (Observed Agreement: 93.3%) |

---

## 2. Distribution Across Topical Domains

| Domain | Count | Percentage |
|---|:---:|:---:|
| `health` | 10 | 16.7% |
| `politics` | 10 | 16.7% |
| `finance` | 10 | 16.7% |
| `disaster` | 10 | 16.7% |
| `sci_tech` | 10 | 16.7% |
| `social` | 10 | 16.7% |

---

## 3. Distribution Across Veracity Classes

| Label | Count | Percentage | Description |
|---|:---:|:---:|---|
| **`REFUTED`** | 21 | 35.0% | Ground-truth adjudicated verdict |
| **`SUPPORTED`** | 13 | 21.7% | Ground-truth adjudicated verdict |
| **`OPINION`** | 11 | 18.3% | Ground-truth adjudicated verdict |
| **`UNVERIFIABLE`** | 8 | 13.3% | Ground-truth adjudicated verdict |
| **`MISLEADING`** | 7 | 11.7% | Ground-truth adjudicated verdict |

---

## 4. Distribution Across Source Mediums

| Source Type | Count | Percentage |
|---|:---:|:---:|
| `social_media` | 38 | 63.3% |
| `news_portal` | 19 | 31.7% |
| `press_release` | 3 | 5.0% |

---

## 5. Temporal Distribution (Publication Year)

| Year | Count | Percentage |
|---|:---:|:---:|
| 2021 | 2 | 3.3% |
| 2022 | 9 | 15.0% |
| 2023 | 35 | 58.3% |
| 2024 | 14 | 23.3% |

---

## 6. Language Variant Breakdown

| Language Variant | Count | Percentage |
|---|:---:|:---:|
| `colloquial_bengali` | 37 | 61.7% |
| `standard_bengali` | 23 | 38.3% |
