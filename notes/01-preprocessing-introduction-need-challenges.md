# Topic 1 — Data Pre-processing: Introduction, Need & Challenges

> **LMS page:** *Chapter 2.1 — Data Pre-processing: Introduction, Need & Challenges* · Course outcome **CO2: analyze the various data pre-processing techniques.**

---

## 1. What is data pre-processing?

**Definition (exam-ready).** Data pre-processing is the set of operations performed on raw data to transform it into a **clean, consistent and usable** form for data mining and machine learning. It sits **between data collection and model building**.

In one line: *pre-processing converts raw, noisy, incomplete data into cleaned, normalized, structured data.*

Three key ideas to remember:
1. It is usually the **most time-consuming step** of any data mining pipeline (60–80 % of project effort).
2. It covers **cleaning, integration, transformation, reduction, discretization, sampling and feature engineering** — that whole family is "pre-processing".
3. Its purpose is not cosmetic: it decides whether the mined pattern is **real** or an **artefact of bad data**.

### The blunt reason it exists

A mining algorithm is a pattern-finding machine with **no common sense**. Feed it `Age = 250`, and it builds a rule around it. Feed it `Income = missing` and it either crashes or silently biases every average. Real data is, without exception:

| Property of real data | What it breaks |
|---|---|
| **Incomplete** (missing attributes, missing values) | averages, distances, model training |
| **Noisy** (random error, sensor jitter, typos) | trend detection, cluster boundaries |
| **Inconsistent** ("M" vs "Male", "Delhi" vs "New Delhi") | grouping, joins, counts |
| **Redundant** (same fact in 3 columns or 2 systems) | model stability, interpretability |
| **Huge** (millions of rows, thousands of columns) | memory, training time |

Hence the oldest law in the field: **Garbage In, Garbage Out (GIGO).** Worse still is *confident* garbage out — a wrong rule with high support that nobody questions.

---

## 2. Why pre-process data? (Need and motivations)

Six motivations, in the order an examiner expects them:

**1. Improve data quality.** Remove errors, inconsistencies, duplicates and noise so that algorithms receive correct, meaningful inputs.

**2. Increase model performance.** Cleaner, well-scaled features yield higher accuracy and better **generalization**; noise reduction lowers **overfitting**.

**3. Ensure compatibility.** Convert heterogeneous sources and formats (databases, CSVs, logs, APIs, spreadsheets) into one consistent format that tools and algorithms accept.

**4. Reduce computational cost.** Dimensionality reduction and sampling cut memory and time requirements — a 1,000-attribute dataset can be 50× slower with no accuracy gain.

**5. Enable correct interpretation.** Well-processed data gives interpretable results and actionable insights; garbage features give unexplainable models.

**6. Compliance and data governance.** Standardize units, anonymize sensitive fields (Aadhaar, phone, card numbers) and satisfy regulatory constraints.

Two supporting motivations worth adding as a sentence each: it **supports downstream tasks** (EDA, visualization, model selection, evaluation all depend on clean data) and it **reduces data quantity** so that mining is feasible at all.

---

## 3. The typical pre-processing pipeline (step by step)

This is the answer to "explain the pre-processing pipeline with a diagram". Memorise the order — marks are given for the sequence.

```
Raw data
   ↓ 1. Data collection & understanding
   ↓ 2. Data integration
   ↓ 3. Data cleaning
   ↓ 4. Data transformation
   ↓ 5. Data reduction
   ↓ 6. Discretization & binning
   ↓ 7. Data splitting (train / validation / test)
   ↓ 8. Verification & validation
   ↓ 9. Documentation
Ready for mining
```

**1. Data collection & understanding.** Inspect sources, data types, volume, variables and domain semantics. Ask: what does each column *mean*, what are its valid ranges, who collected it?

**2. Data integration.** Combine multiple sources and reconcile schema differences (names, types, units, conflicts).

**3. Data cleaning.** Handle missing values, noisy entries, inconsistencies, duplicates and erroneous records.

**4. Data transformation.** Normalization/standardization, scaling, encoding categorical variables, feature construction.

**5. Data reduction.** Dimensionality reduction, feature selection, sampling, aggregation.

**6. Discretization & binning.** Convert continuous features into intervals where required.

**7. Data splitting.** Train/validation/test split or cross-validation partitions. **Split before fitting any transformation** — this is the step students skip and then report fake accuracy.

**8. Verification & validation.** Re-check statistical properties, distributions and integrity *after* processing (a mean that moved from 34 to 340 means a scaling bug).

**9. Documentation.** Record steps, code and rationale for reproducibility and audit. In industry this is a legal requirement for credit/medical models.

### The four families (a clean way to hold the whole unit in your head)

| Family | Question it answers | Techniques | LMS page |
|---|---|---|---|
| **Cleaning** | Is the data correct and complete? | missing values, noise, outliers, duplicates | 2, 3 |
| **Integration** | Is the data unified? | schema matching, redundancy removal | 4 |
| **Reduction** | Is the data too big? | cube aggregation, dimensionality reduction, sampling, attribute subset selection | 5, 6 |
| **Transformation** | Is the data in usable form? | normalization, encoding, concept hierarchy, discretization | 7, 8 |

Everything in Unit 2 belongs to one of these four columns, and association-rule mining (topics 9–13) is what you *do* with the resulting clean data.

---

## 4. Core pre-processing tasks (detailed summary)

### 4.1 Data cleaning
- **Missing values** — delete tuples, impute mean/median/mode, class-based imputation, KNN, regression, model-based (EM, MICE).
- **Noise smoothing** — binning, regression, moving average, clustering-based smoothing.
- **Outlier detection** — z-score, IQR/boxplot, DBSCAN/clustering, isolation forest; then decide **remove, cap or keep** with justification.
- **Inconsistencies** — fix format mismatches (dates, units), map synonyms, enforce domain constraints.
- **Duplicate detection / record linkage** — exact match, fuzzy string matching, phonetic algorithms (Soundex), composite keys.

### 4.2 Data integration
- **Schema matching** — align column names and types.
- **Entity resolution** — deduplicate the same real-world object across sources.
- **Conflict resolution** — pick the authoritative source, or apply majority/weighted rules.
- **Unit standardization** — e.g. all temperatures to °C.
- **Timestamp/frequency alignment** — resample time series to a common frequency.

### 4.3 Data transformation
- **Scaling:** min–max normalization → [0, 1] (sensitive to outliers); z-score standardization → mean 0, sd 1.
- **Encoding:** label encoding (ordinal), one-hot encoding (nominal), target/frequency encoding (watch leakage).
- **Feature construction:** interaction terms, polynomial features, date/time decomposition (day, month, weekday, is_holiday), aggregates.
- **Distribution shaping:** log/power transforms to reduce skewness.
- **Feature hashing** for very high-cardinality categorical fields.

### 4.4 Data reduction
- **Feature selection:** filter (correlation, χ², mutual information), wrapper (RFE), embedded (Lasso, tree importance).
- **Dimensionality reduction:** PCA, SVD, LDA, t-SNE/UMAP (visualization), autoencoders.
- **Sampling:** random, stratified, systematic, cluster, reservoir, importance.
- **Aggregation/binning:** transactional data to customer level; continuous to intervals.

### 4.5 Discretization & binning
Equal-width, equal-frequency, k-means, and entropy-based (supervised) discretization. Needed when an algorithm requires categorical input or when you want interpretable rules like *"age between 25 and 40"*.

---

## 5. Practical techniques the LMS notes list (know the names + one line)

| Technique | What it does | Caveat |
|---|---|---|
| **KNN imputation** | fills missing values from the k most similar complete records | expensive on large data |
| **Regression imputation** | predicts the missing value from other attributes | assumes a linear relation |
| **EM (Expectation–Maximization)** | iteratively estimates the most likely values under an assumed distribution | slow, needs distributional assumption |
| **SMOTE / ADASYN** | synthesizes minority-class samples for class imbalance | can create unrealistic points |
| **PCA** | keeps variance while reducing dimensions | linear, unsupervised, needs scaling |
| **One-hot vs target encoding** | one-hot avoids leakage but explodes dimensions; target encoding is compact but needs careful cross-validation | leakage risk both ways |

---

## 6. How to evaluate a pre-processing choice

Never claim "pre-processing improved the model" without evidence. Three checks:

**1. Before/after statistics.** Mean, standard deviation, skew, min/max; distribution plots (histogram, boxplot); correlation heatmap. A number that became impossible (negative count, age 900) means a bug.

**2. Model-based evaluation.** Train a simple baseline **before** and **after** pre-processing; compare accuracy, RMSE, AUC. This converts opinion into measurement.

**3. Leakage check.** Fit transforms **only on the training fold**; apply to validation/test. Cross-validate the *whole pipeline* (scaling + imputation + model), not just the model.

---

## 7. Common challenges and their solutions (nine, straight from the LMS page)

| # | Challenge | Why it hurts | Solution |
|---|---|---|---|
| 7.1 | **Missing data** | deletion biases results when a large fraction is missing | model-based/multiple imputation; identify MCAR / MAR / MNAR first |
| 7.2 | **High dimensionality (curse of dimensionality)** | overfitting, slow computation, distances lose meaning | feature selection, PCA, regularization, domain knowledge |
| 7.3 | **Noisy and erroneous data** | unstable models, wrong trends | robust smoothing, outlier detection, validation rules |
| 7.4 | **Class imbalance** | minority class ignored; accuracy misleading | resampling (over/under), SMOTE, metrics = precision/recall/F1/ROC-AUC |
| 7.5 | **Integration conflicts** | two sources disagree about the same entity | source weighting, provenance tracking, business rules |
| 7.6 | **Leakage during pre-processing** | optimistic (fake) accuracy | fit on train only; apply the same transformer to test |
| 7.7 | **Large datasets / scalability** | memory-bound, too slow | incremental/mini-batch algorithms, Spark, feature hashing, streaming imputation |
| 7.8 | **High-cardinality categoricals** | one-hot explodes dimensionality | target/frequency encoding, hashing trick, embeddings, group rare categories |
| 7.9 | **Temporal / time-series issues** | non-stationarity, seasonality, irregular sampling | resampling, temporal-neighbour imputation, detrending, seasonal decomposition |

**Two traps examiners love**
1. **Leakage:** computing the scaler or imputer on the full dataset leaks test information into training. Correct order: split → `fit_transform` on train → `transform` on test.
2. **Deleting signal:** missingness is itself information (a blank income field correlates with low income). Deleting every incomplete row biases the sample; sometimes an `is_missing` flag is the better fix.

---

## 8. Where this unit sits in the KDD process

```
Raw data → (1) Cleaning → (2) Integration → (3) Reduction → (4) Transformation
        → (5) Data mining → (6) Pattern evaluation → (7) Knowledge presentation
```

Steps 1–4 are exactly this unit. If asked *"explain the role of pre-processing in KDD"*, draw this chain and state that steps 1–4 are pre-processing, and that mining (step 5) is only as good as its input.

---

## 9. One-paragraph summary for revision

Pre-processing converts raw data into a clean, consistent, compact, usable form. It is needed to improve quality, model performance, compatibility, computational cost, interpretability and compliance. It follows a nine-step pipeline (understand → integrate → clean → transform → reduce → discretize → split → verify → document) and consists of four families: cleaning, integration, reduction and transformation. Its biggest risks are data leakage (fitting transforms on the test set) and destroying signal (deleting all incomplete records); both are avoided by splitting first, fitting on training data only, and validating the whole pipeline with cross-validation.

---
**Next:** [Topic 2 — Data Cleaning: Missing Values & Noise Handling](02-data-cleaning-missing-values-noise.md)
