# Unit 2 — Data Preprocessing & Association Rules · REVISION SHEET

## 1. Core definitions (learn word-for-word)

- **Pre-processing:** operations on raw data that turn it into a clean, consistent, usable form for mining; sits between collection and model building; 60–80 % of project effort.
- **Data cleaning:** identifying and correcting errors, inconsistencies and inaccuracies.
- **Missing value:** no data stored for an attribute in an observation. **MCAR** (random) · **MAR** (depends on other observed attributes) · **MNAR** (depends on the value itself).
- **Noise:** random error/fluctuation that obscures pattern. **Outlier:** a value far from the rest — may be noise *or* a genuine rare event.
- **Data integration:** combining multiple sources into one unified view (schema integration + redundancy removal).
- **Redundancy:** the same information stored in several attributes/records. Detected by **correlation (numeric)**, **χ² (nominal)**, **ANOVA (numeric vs nominal)**.
- **Data reduction:** shrink the dataset while preserving its essential patterns.
- **Data cube:** multidimensional structure (dimensions × measures); levels = **base → intermediate → apex**; OLAP = **roll-up, drill-down, slice, dice, pivot**.
- **Sampling:** selecting a representative subset. Needs **representativeness** + **adequate size**.
- **Attribute subset selection:** keep only relevant original attributes.
- **Normalization:** rescale numerics to a standard scale. **Encoding:** convert categories to numbers.
- **Discretization:** continuous → intervals. **Binarization:** two intervals.
- **Concept hierarchy:** values organised specific → general (city → state → country).
- **Frequent itemset:** itemset with `support ≥ minsup`. **Association rule:** `X → Y`, `X ∩ Y = ∅`.

## 2. All the formulas

| Quantity | Formula |
|---|---|
| **Support** | `s(X) = σ(X)/N` |
| **Confidence** | `c(X→Y) = σ(X∪Y)/σ(X)` |
| **Lift** | `s(X∪Y)/(s(X)·s(Y))` — 1 = independent, >1 positive, <1 negative |
| **Leverage** | `s(X∪Y) − s(X)s(Y)` |
| **Conviction** | `(1 − s(Y))/(1 − c(X→Y))` |
| **Min–max** | `(v − min)/(max − min)` → [0,1] |
| **Z-score** | `(v − μ)/σ` → mean 0, sd 1 |
| **Decimal scaling** | `v / 10^j`, smallest j with `max|v'| < 1` |
| **Robust scaling** | `(v − median)/IQR` |
| **IQR bounds** | `Q1 − 1.5·IQR`, `Q3 + 1.5·IQR` |
| **z-score test** | `|z| > 3` → outlier |
| **Entropy** | `−Σ pᵢ log₂ pᵢ` · **Gain** = `E(S) − Σ(|Sᵥ|/|S|)E(Sᵥ)` |
| **Gini** | `1 − Σ pᵢ²` |
| **Pearson r** | `Σ(aᵢ−Ā)(bᵢ−B̄) / ((n−1)σ_Aσ_B)` |
| **χ²** | `Σ(obs−exp)²/exp`, `exp = (row×col)/grand` |
| **Sample size (mean)** | `n = (Zσ/E)²` · (proportion) `n = Z²p(1−p)/E²` |
| **Standard error** | `SE = σ/√n` |
| **Moving average** | `MA(3)ₜ = (aₜ + aₜ₋₁ + aₜ₋₂)/3` |
| **Rules from a k-itemset** | `2^k − 2` |

## 3. Comparison tables (the marks live here)

**Apriori property:** if an itemset is **infrequent, all its supersets are infrequent** ⇒ `σ(superset) ≤ σ(subset)`. Called **anti-monotonic / downward closed**.

**Apriori vs FP-Growth**

| Apriori | FP-Growth |
|---|---|
| candidate generation + pruning | **no candidates** |
| `k_max + 1` DB scans | **2 scans** |
| simple, exact | complex, exact |
| slow on dense/long data | **fast** on dense data |
| memory: candidate sets | memory: **FP-tree must fit in RAM** |

**Filter vs Wrapper vs Embedded**

| Filter | Wrapper | Embedded |
|---|---|---|
| statistical score, no model | retrains a model per subset | selection inside training |
| fast, ignores interactions | accurate, very slow | good trade-off |
| corr, χ², MI, ANOVA | forward, backward, RFE | Lasso, tree importance |

**Feature selection vs feature extraction:** selection keeps original attributes (meaning preserved); extraction creates new ones (PCA, SVD, LDA) — compact but uninterpretable.

**Discretization:** unsupervised = equal-width, equal-frequency, k-means · supervised = entropy/MDLP, χ²/ChiMerge, CART/Gini · top-down = split, bottom-up = merge.

**Encoding:** ordinal → label/ordinal · small nominal → one-hot · high cardinality → frequency/target/binary/hashing · boosting → target encoding (out-of-fold!).

**Missing values:** delete row / delete column → constant / mean / median / mode → class-based / KNN / regression / MICE / EM / autoencoder.

**Outliers:** statistical (z-score, IQR, boxplot) · distance (kNN) · density (DBSCAN, LOF) · model (Isolation Forest, One-Class SVM).

**Smoothing:** binning (mean/median/boundary), regression, moving average, LOWESS, clustering, median filter.

**Sampling:** random (SRSWOR/SRSWR), stratified, systematic, cluster, reservoir, multistage, progressive.

**Never forget:** fit every transform on **train only** — otherwise leakage.

## 4. Mnemonics

- **Data quality — ACCTBI:** **A**ccuracy, **C**ompleteness, **C**onsistency, **T**imeliness, **B**elievability, **I**nterpretability.
- **Pre-processing pipeline — 9 steps:** Understand → Integrate → Clean → Transform → Reduce → Discretize → Split → Verify → Document.
- **Missingness — C-A-N:** MCAR / MAR / MNAR = **C**ompletely random / **A**t random (other attributes) / **N**ot at random (the value itself).
- **Interestingness — SCL:** **S**upport (coverage), **C**onfidence (reliability), **L**ift (beyond chance).
- **Apriori loop — JPC:** **J**oin → **P**rune → **C**ount.
- **FP-Growth — CCM:** **C**ount items → **C**onstruct tree (2nd scan) → **M**ine conditional bases bottom-up.

## 5. Ten sentences that earn marks

1. A superset can never be more frequent than its subset — this is why Apriori prunes.
2. Noise is random error spread over many records; an outlier is one extreme record that may be the finding, not the fault.
3. Lift = 1 means independence; lift > 1 means the antecedent raises the chance of the consequent.
4. Confidence is directional; lift is symmetric.
5. Mean imputation shrinks variance; median is the correct choice for skewed data.
6. Equal-width binning is outlier-sensitive; equal-frequency is not.
7. Supervised discretization (entropy) beats unsupervised because boundaries are chosen to separate classes.
8. FP-Growth trades two scans and a tree in memory against Apriori's repeated scans and candidate explosion.
9. High confidence with low support is a cross-support artefact, not a business rule.
10. Any transformation fitted on the full dataset leaks test information and inflates accuracy.

## 6. Numbers to remember

| Item | Value |
|---|---|
| 95 % confidence Z | **1.96** |
| Outlier z-score threshold | **±3** |
| IQR multiplier | **1.5** (extreme: 3) |
| Strong correlation | `|r| > 0.9` |
| Typical keep-variance for PCA | **90–95 %** |
| Column deletion threshold (LMS) | **> 70 % missing** |
| χ² 5 % critical value, 1 df | **3.84** |
| Useful minsup range (practice) | 0.01–0.10 for large data |

---
**Full explanations:** [notes/](../notes/) · **Practice:** [question-bank.md](question-bank.md)
