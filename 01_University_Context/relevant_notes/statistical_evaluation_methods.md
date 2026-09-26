# Statistical Evaluation & Hypothesis Testing Protocol
## Context Derived from AIUB MAT 3103 (Computational Statistics & Probability)

This document formalizes the inferential statistics protocol drawn from AIUB course MAT 3103 (`G:\AIUB\24 - 3 - Semester 4\Math 6 Mortuza Sir\MAT 3103 Computational Statistics & Probability (FALL_24-25).docx`).

---

## 1. Problem Formulation: Statistical Significance in NLP Evaluation

A frequent deficiency in empirical NLP studies is reporting absolute metric differences (e.g., Model A scores 78.4% F1 vs. Model B scores 77.1% F1) without assessing whether the difference is statistically distinguishable from random chance. 

Following AIUB MAT 3103 modules on hypothesis testing, confidence intervals, and inferential decision rules, BanglaFactBench mandates explicit statistical testing.

---

## 2. Hypothesis Testing Formulation

For any paired comparison between Model $M_A$ and Model $M_B$:
- **Null Hypothesis ($H_0$)**: There is no difference in verification accuracy/macro-F1 between $M_A$ and $M_B$ ($\mu_A - \mu_B = 0$).
- **Alternative Hypothesis ($H_1$)**: Model $M_A$ outperforms Model $M_B$ ($\mu_A - \mu_B \neq 0$ or $\mu_A > \mu_B$).
- **Significance Level**: $\alpha = 0.05$ (standard), with Bonferroni correction for multiple testing: $\alpha' = \alpha / k$.

---

## 3. Mandatory Statistical Tests

### 3.1 Paired McNemar's Test for Categorical Predictions
For comparing two classifiers on the exact same test dataset of $N$ claims:
Construct the contingency table of binary correctness:

| | $M_B$ Correct | $M_B$ Incorrect |
|---|---|---|
| **$M_A$ Correct** | $n_{00}$ | $n_{01}$ |
| **$M_A$ Incorrect** | $n_{10}$ | $n_{11}$ |

The McNemar test statistic with Edward's continuity correction is:
$$\chi^2 = \frac{(|n_{01} - n_{10}| - 1)^2}{n_{01} + n_{10}}$$
Under $H_0$, $\chi^2$ follows a chi-squared distribution with 1 degree of freedom. Reject $H_0$ if $p < 0.05$.

### 3.2 Non-Parametric Bootstrap Confidence Intervals
To compute 95% confidence intervals for Macro-F1:
1. Resample with replacement $B = 1000$ bootstrap datasets $D_1^*, \dots, D_B^*$ from the test set $D_{\text{test}}$.
2. Evaluate Macro-F1 on each bootstrap sample: $\theta_b^* = \text{Macro-F1}(D_b^*)$.
3. Compute the empirical 2.5th and 97.5th percentiles:
   $$\text{CI}_{95\%} = [\theta_{(0.025)}^*, \, \theta_{(0.975)}^*]$$
4. Report: $\text{Macro-F1} = \bar{\theta} \pm \Delta$ alongside the empirical confidence interval.

### 3.3 Inter-Annotator Agreement Statistics
- **Cohen's Kappa ($\kappa$)** for pairwise annotation:
  $$\kappa = \frac{P_o - P_e}{1 - P_e}$$
  where $P_o$ is the observed proportional agreement and $P_e$ is the expected agreement by chance under marginal distributions.
- **Interpretation Matrix (Landis & Koch, 1977)**:
  - $< 0.00$: Poor
  - $0.00 - 0.20$: Slight
  - $0.21 - 0.40$: Fair
  - $0.41 - 0.60$: Moderate
  - $0.61 - 0.80$: Substantial
  - $0.81 - 1.00$: Almost Perfect
  *Note: Kappa is never fabricated; it is calculated exclusively from completed human annotations.*
