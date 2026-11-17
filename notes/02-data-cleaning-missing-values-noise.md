# Topic 2 — Data Cleaning: Missing Values & Noise Handling

> **LMS page:** *Chapter 2.1 — Data Cleaning: Missing Values, Noise Handling* · **CO2**

---

## 1. What data cleaning is

**Definition.** Data cleaning is the process of **identifying and correcting errors, inconsistencies and inaccuracies** in a dataset. It is the first and most crucial part of pre-processing because mining algorithms rely entirely on the quality of the input.

The two major problems handled here are **missing values** and **noise**. (Outliers and smoothing are the next topic.)

**Where the dirt comes from:** improper data entry, sensor malfunction, users skipping questions, lost/corrupted files, and mismatched schemas during integration.

---

## 2. Missing values

**Definition.** A missing value occurs when **no data is stored for an attribute in an observation** — the cell is empty, `NULL`, `NaN`, `-`, `?`, or a placeholder like `999`.

Missing values are dangerous in three different ways: they **reduce sample size**, they **bias statistics** (the mean of the observed values is not the mean of the population), and they **break algorithms** that cannot handle `NaN`.

### 2.1 The three types of missingness (MCAR, MAR, MNAR) — always identify this first

| Type | Full form | Meaning | Example | Safe strategy |
|---|---|---|---|---|
| **MCAR** | Missing Completely At Random | missingness has **no relationship** to any data, observed or not | a machine temporarily fails to record temperature | deletion is unbiased (just wasteful); simple imputation fine |
| **MAR** | Missing At Random | missingness depends on **other observed attributes**, not on the missing value itself | younger customers skip the income field | imputation using other attributes (regression, KNN, class-based) is valid |
| **MNAR** | Missing Not At Random | missingness depends on **the missing value itself** | high earners refuse to report income | hardest case; needs advanced/ model-based imputation or an explicit "missing" category; deletion biases the result |

> **Why this matters:** the *same* technique is correct under MCAR and wrong under MNAR. Saying this in an answer is what separates a good answer from a list of techniques.

### 2.2 Techniques for handling missing values

**A. Deletion methods**

| Method | How | Use when | Drawback |
|---|---|---|---|
| **Remove tuple (record deletion / listwise deletion)** | delete every row containing a missing value | dataset is large and only a small % of values are missing | can lose important patterns; biased if missingness is not MCAR |
| **Remove attribute (column deletion)** | delete the whole column | a very large share is missing (LMS guide: **over ~70 %**) | may throw away a genuinely useful feature |

**B. Imputation methods** (fill the gap with a plausible value)

| Method | How | Advantages | Drawbacks |
|---|---|---|---|
| **Global constant** | replace with `"Unknown"`, `0`, `-1` | simple; works for categorical; missingness stays visible | may create a new misleading category; distorts distances if the constant is extreme |
| **Mean imputation** | fill with the attribute mean | simple, fast; fine for symmetric numeric data | shrinks variance, ignores correlations, sensitive to outliers |
| **Median imputation** | fill with the median | robust for **skewed** data and outliers | still ignores relationships |
| **Mode imputation** | fill with the most frequent value | the standard choice for **categorical** attributes | may over-represent the majority category |
| **Class-based (group-wise) imputation** | compute mean/median/mode **within each class** (e.g. mean age of males for a male record) | more accurate than a global mean; preserves class structure | needs enough data per class |
| **KNN imputation** | average the values of the **k most similar complete records** | maintains relationships between variables | computationally expensive on large data; needs a distance measure |
| **Regression imputation** | predict the missing value from other attributes, e.g. `Age = a + b·Education + c·Income` | more realistic than a constant | assumes a (usually linear) relationship; can over-shrink variance |
| **MICE** (Multiple Imputation by Chained Equations) | iterate regression imputations across all attributes, producing several completed datasets | preserves variance and correlation structure; industry standard | complex, needs statistical tooling |
| **EM (Expectation–Maximization)** | iteratively estimate the most likely values under an assumed distribution (E-step estimates, M-step re-estimates parameters) | statistically principled | slow; distributional assumption |
| **Deep-learning autoencoders** | learn the data manifold and reconstruct missing entries | best for images/complex high-dimensional data | needs lots of data, a black box |

**C. Do nothing (model-native handling).** Some algorithms handle missingness natively: C4.5/XGBoost/LightGBM learn a default direction for missing values; some databases treat `NULL` as a category. Fast, but only valid for those models.

### 2.3 Best practices for missing values (from the LMS page — reproduce these)

1. **Analyse the missingness pattern before choosing a method** (MCAR/MAR/MNAR, and whether missingness correlates with the target).
2. **Never apply imputation blindly** — understand *why* the value is missing.
3. **Document** which method was used and why (reproducibility).
4. **Use cross-validation** to check whether the imputation actually improved model performance.
5. **Avoid mean imputation for skewed data** — use median.
6. **For MNAR, prefer advanced imputation** (model-based / multiple imputation), never deletion.

Two more worth adding: consider an **`is_missing` indicator column** when missingness is predictive, and **never impute using statistics from the test set** (leakage).

---

## 3. Noise in data

**Definition.** Noise refers to **random errors, fluctuations or meaningless information** that distort data patterns.

**Examples.** Sensor malfunction producing spikes; human typing errors (`age 256` instead of `26`); random fluctuations in stock prices; a rounded-down salary field.

**Why it matters.** Noise misleads clustering (blurred boundaries), regression (wrong slope), classification (wrong split) and association mining (spurious rules).

### 3.1 Types of noise (LMS list)

1. **Random noise** — unpredictable fluctuation; common in sensor and transaction data.
2. **Systematic noise (bias)** — a consistent error from instrument bias or a miscalibrated scale.
3. **Outliers** — extreme values far from the majority (treated in detail in Topic 3).
4. **Duplicate or redundant data** — repeated entries that distort frequency counts and averages.

### 3.2 Noise-handling (smoothing) techniques

**1. Binning (smoothing by bins).** Sort the values, divide into equal-size bins, then replace each value with a bin representative:
- **By bin mean**, **by bin median**, or **by bin boundaries** (nearest boundary).

*LMS example:* `Ages = [20, 21, 19, 55, 56, 54]` → Bin 1 = [19, 20, 21], Bin 2 = [54, 55, 56]; smooth each bin by its median → Bin 1 becomes 20, 20, 20; Bin 2 becomes 55, 55, 55.
*Advantage:* simple and effective at removing local fluctuation.

**Full worked binning example** (equal-frequency, 3 bins) on sorted values `4, 8, 9, 15, 21, 21, 24, 25, 28, 34`:

| Smoothing | Bin 1 {4,8,9,15} | Bin 2 {21,21,24,25} | Bin 3 {28,34} |
|---|---|---|---|
| **By bin mean** | 9, 9, 9, 9 | 22.75 × 4 | 31, 31 |
| **By bin median** | 8.5 × 4 | 22.5 × 4 | 31, 31 |
| **By bin boundary** (boundaries are the bin min/max) | 4, 4, 4, 15 | 21, 21, 25, 25 | 28, 28, 34, 34 |

**2. Regression smoothing.** Fit a line/curve and replace each value with the fitted value. Types: **linear** and **polynomial** regression. Used for trend smoothing and stock-market series; effective when noise is added on top of a smooth trend.

**3. Moving average / rolling window.** Replace a value by the average of its neighbours: `MA(3) at t = (x(t) + x(t−1) + x(t−2)) / 3`. Standard for time series; removes peaks and shows trend. Cost: lags the series and flattens genuine sharp changes.

**4. LOWESS / LOESS.** Locally weighted regression: fits a smooth curve giving **more weight to nearby points**. Handles complex, non-linear patterns that a global regression misses.

**5. Clustering-based noise detection.** Cluster first (k-means, DBSCAN); points **far from centroids**, or points forming **tiny clusters of their own**, are noise and can be smoothed or removed.

**6. Outlier detection and removal.** z-score, IQR/boxplot, density-based (DBSCAN), Isolation Forest. Detected outliers may be **removed, capped, or replaced with the nearest neighbours** (see Topic 3).

---

## 4. Noise vs outlier — the table examiners ask for

| Noise | Outlier |
|---|---|
| Random error in values | An extreme, unusual data point |
| Happens frequently, affects many records | Rare |
| Handled by **smoothing** (binning, moving average, regression) | Handled by **detection** (z-score, IQR, LOF, isolation forest) |
| Small deviation, hard to interpret | Often meaningful (fraud, disease, equipment failure) |

One-line summary: *noise is a small random error spread across many records; an outlier is one extreme record, which may be noise or may be the discovery.*

---

## 5. Why noise handling is important

- Improves model **accuracy** (the model learns the pattern, not the jitter).
- **Reduces overfitting** — noisy data makes a model memorize noise.
- **Clarifies cluster boundaries** (k-means and DBSCAN stop chasing stray points).
- **Reveals the true trend** in time series and regression.
- **Prevents misleading predictions** downstream (forecast, risk score, recommendation).

---

## 6. Worked combined example (LMS "data cleaning in one pass")

Dataset:

| Age | Income | Gender |
|---|---|---|
| 25 | 50,000 | M |
| ? | 75,000 | Male |
| 250 | 60,000 | M |
| 30 | ? | F |
| 25 | 50,000 | M |

Cleaning steps, in order:
1. **Standardize categories:** `M` and `Male` → `M` (consistency).
2. **Impute missing Age** with the median (median of 25, 250, 30, 25 = 27.5 — state the value you computed; note that the median is chosen precisely because the 250 would destroy a mean).
3. **Detect the outlier** `Age = 250` (outside IQR bounds; a z-score will *not* catch it because the outlier inflates σ — see Topic 3) → correct if a typo (25), else cap to a plausible maximum.
4. **Impute missing Income** with regression/KNN rather than the plain mean (income correlates with age).
5. **Remove the duplicate row** (rows 1 and 5 are identical).

> Notice the order matters: standardize and fix outliers **before** computing an imputation statistic, otherwise a 250-year-old inflates the mean used to fill the gap.

---

## 7. Summary paragraph

Missing values occur through entry errors, sensor failure and schema mismatch, and are classified as **MCAR, MAR or MNAR** — the classification decides whether deletion is safe or advanced imputation is required. Handling methods run from deletion (tuple/attribute) through simple imputation (global constant, mean, median, mode), to context-aware imputation (class-based, KNN, regression) and modern methods (MICE, EM, autoencoders). Noise is random error that obscures pattern; it is reduced by binning, regression, moving average, LOWESS and clustering-based smoothing, and removed from individual records by outlier detection. The guiding rule for both: **understand the mechanism first, measure the effect afterwards, and never compute a statistic on data you are about to test on.**

---
**Next:** [Topic 3 — Data Cleaning: Outlier Detection & Smoothing](03-data-cleaning-outliers-smoothing.md)
