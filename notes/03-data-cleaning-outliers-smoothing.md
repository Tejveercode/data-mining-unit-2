# Topic 3 — Data Cleaning: Outlier Detection & Smoothing

> **LMS page:** *Chapter 2.1 — Data Cleaning: Outlier Detection, Smoothing* · **CO2**

---

## 1. What is an outlier

**Definition.** Outliers are data points that **deviate significantly from the rest of the dataset** — unusually large or small values compared with typical observations. They may indicate **errors, rare events, anomalies, or genuine but unusual behaviour**.

Outlier detection matters because outliers **distort statistical measures, mislead mining algorithms and reduce model accuracy**.

## 2. Why outliers occur

| Cause | Example |
|---|---|
| **Human error** | mistyping 250 for 25; mislabelling a category |
| **Instrument / sensor malfunction** | a spike to 999 °C for one reading |
| **Natural variability** | a genuine rare event — a billionaire's income, a once-in-a-century rainfall |
| **Data integration issues** | unit conversion mismatch (kg vs lb), format mismatch |
| **Fraud or malicious activity** | a card suddenly used in two countries |

> Key insight: an outlier is **not automatically an error**. Before removing anything, ask *"is this a mistake, or is this the finding?"* In fraud detection, network intrusion, disease outbreak and equipment-failure mining, **the outlier is the target**.

## 3. Types of outliers

| Type | Definition | Example |
|---|---|---|
| **Global (point) outlier** | far from **all** other observations | salary of 10 million where typical is 20,000–50,000 |
| **Contextual (conditional) outlier** | unusual **only in a specific context** | temperature 30 °C is normal in summer, abnormal in winter |
| **Collective outlier** | a **group** of points that is unusual together, though each point alone looks fine | a run of very low sensor readings indicating a device fault |

Two more names worth knowing: **micro-outlier** (tiny deviation) vs **macro-outlier** (extreme); and **local outlier** (compared with its neighbourhood, not the whole dataset — the idea behind LOF).

## 4. Effects of outliers on data mining

- **Statistics:** mean and standard deviation become unreliable (one billionaire raises the "average" income of a village).
- **Regression:** the fitted line is pulled toward the extreme value — the slope can even flip sign.
- **Clustering:** k-means forms a cluster around the outlier or merges real clusters to compensate.
- **Classification:** decision boundaries shift, so accuracy drops on normal data.
- **Association mining:** rules built from an outlier transaction look strong but generalize to nobody.
- **Neural networks / gradient training:** a huge value produces a huge gradient → unstable training.

## 5. Outlier detection techniques (four families)

### 5.1 Statistical methods

**Z-score method.** Measures how many standard deviations a value lies from the mean:
```
z = (x − μ) / σ          flag as outlier if |z| > 3
```
*Example:* μ = 40, σ = 5, x = 65 → z = (65 − 40)/5 = 5 → outlier.
*Limitations:* assumes (roughly) a normal distribution and is itself computed from the mean/σ, which outliers distort; on skewed data (income) it flags perfectly normal high values. Use the **modified z-score** (median/MAD) for robustness.

**IQR (interquartile range) method** — the boxplot rule, distribution-free:
```
IQR = Q3 − Q1
Lower bound = Q1 − 1.5·IQR
Upper bound = Q3 + 1.5·IQR
```
Any value outside the bounds is an outlier; values beyond `3·IQR` are **extreme** outliers.
*Example:* Q1 = 20, Q3 = 40 → IQR = 20 → bounds = [−10, 70]; any value > 70 or < −10 is an outlier.

**Boxplot detection.** The visual version: the box spans Q1–Q3, whiskers extend to 1.5·IQR, points beyond the whiskers are plotted individually. Fast, and easy to draw in an exam.

**Grubbs' test / Dixon's Q test.** Formal statistical hypothesis tests for a single outlier in a normal sample.

### 5.2 Distance-based methods

- **Euclidean distance:** points far from all others (a large distance to the nearest neighbour) are outliers. Effective for numeric features, but every attribute must be on a comparable scale.
- **KNN distance:** a point whose **average distance to its k nearest neighbours** is much larger than the average over the dataset is an outlier (the k-NN outlier factor).
- **Formal definition (Knorr & Ng):** an object is an outlier if **at least p % of the objects are further than distance d** from it — the two parameters (p, d) are the tuning knobs.

### 5.3 Density-based methods

- **DBSCAN:** clusters are dense regions; points in **low-density regions** (not reachable from any core point) are labelled **noise**. No need to pre-specify k.
- **Local Outlier Factor (LOF):** compares a point's local density with the densities of its neighbours. `LOF ≈ 1` → normal; `LOF ≫ 1` → the point is isolated relative to its neighbourhood. **Handles clusters of different densities** and detects *local* outliers that global methods miss.

### 5.4 Model-based (machine-learning) methods

- **Isolation Forest:** repeatedly splits the data with random cuts. Outliers are isolated in **fewer splits** (shorter path length) — so unusual points are easy to separate. Fast, scales to millions of rows, works in high dimensions.
- **One-Class SVM:** learns a boundary around the normal data; anything outside is an anomaly. Needs mostly-clean training data.
- **Autoencoder / reconstruction error:** train a network to reproduce normal records; records with high reconstruction error are anomalies (used in modern fraud/intrusion detection).
- **Clustering-based:** points in no cluster, or far from their centroid (> 3σ), are outliers.

---

## 6. Outlier treatment (what to do after detection)

| Treatment | When | Effect |
|---|---|---|
| **Removal** | proven to be an error and not meaningful | clean but loses information; changes the distribution |
| **Capping / winsorizing** | genuine but extreme values you don't want driving the model | keeps the record, limits influence (e.g. cap at the 99th percentile) |
| **Transformation** | heavy-tailed / skewed data | log or square-root compresses extremes |
| **Replacement** | value is known to be wrong but the record matters | replace with median, mean or nearest neighbour |
| **Treat as a separate class** | outliers represent meaningful rare events (fraud, disease) | mines them instead of deleting them |
| **Robust methods** | you want to keep the data untouched | use median/IQR, robust scaling, tree models (insensitive to monotone transforms) |

**Decision rule for the exam:** *"remove if erroneous, cap or transform if genuine but extreme, keep and model if the rare event is the business interest."*

---

## 7. Smoothing

**Definition.** Smoothing is the process of **reducing noise or random fluctuations** in the data. Noise is unwanted variation that hides important patterns; smoothing produces a clean signal, clearer trends and more stable models.

### 7.1 Why smoothing is needed
- Noise distorts statistical summaries and visualizations.
- Models become unstable when trained on noisy data.
- Time-series forecasts become inaccurate with random spikes.
- Noise **hides real trends** and patterns.

### 7.2 Smoothing techniques

**1. Binning (smoothing by partitioning).** Sort the data, divide into equal-size bins, replace values by:
- **bin mean** — each value → mean of its bin;
- **bin median** — each value → median of its bin;
- **bin boundaries** — each value → the nearer of the bin's minimum/maximum.

*Simple and useful for removing small variations.* (Worked table in Topic 2, §3.2.)

**2. Regression smoothing.** Fit a function (linear or polynomial) to the data and replace values by the fitted values. Effective when data follows a trend or curve; reduces noise in continuous variables.

**3. Moving average smoothing.** Replace each value by the average of its neighbours:
```
MA(3) at t = (A(t) + A(t−1) + A(t−2)) / 3
```
Reduces sudden jumps; shows a smoother trend. Mainly for time series. Variants: weighted moving average (recent points weighted more), exponential smoothing (`S(t) = α·A(t) + (1−α)·S(t−1)`).

**4. LOWESS / LOESS.** Locally weighted regression: fits a smooth curve by giving **more weight to nearby points**. Handles complex non-linear patterns; needs no global functional form.

**5. Clustering-based smoothing.** k-means/DBSCAN group similar points; points far from cluster centres are treated as noise and smoothed or removed.

**6. Median filter.** Replace each value with the median of a small window — excellent for removing salt-and-pepper spikes without blurring edges (standard in image processing).

### 7.3 Outlier handling vs smoothing — the comparison the LMS page makes

| Outlier handling | Smoothing |
|---|---|
| Focuses on **individual points** that deviate | Deals with **random fluctuation across all points** |
| Identifies rare/extreme values | Reduces the overall noise level |
| Action: remove, cap, replace | Action: transform every value toward its neighbours |
| Metric: z-score, IQR, LOF | Metric: bin statistic, moving average, fitted curve |

Both improve data quality but act on **different types of error**: outliers are the few *wrong* points, noise is the many *slightly imprecise* points.

---

## 8. Worked example (numeric, exam style)

Values: `12, 14, 13, 12, 15, 95, 13, 14, 12, 13`

**Step 1 — detect.** Mean = 21.3, σ ≈ 25.5 → z(95) = (95 − 21.3)/25.5 = 2.89. Borderline by z-score (note how the outlier inflates σ and hides itself — a great point to make). IQR: sorted → Q1 = 12.25, Q3 = 14 → IQR = 1.75 → upper bound = 14 + 2.625 = **16.6** → **95 is clearly an outlier**.

**Step 2 — treat.** Options: remove it (mean becomes 13.1, σ ≈ 1.0 — the honest summary), cap it at 16.6, or log-transform. Each is defensible **if justified**: 95 is implausible for "hours studied per week", so removal/correction is right; for "customer spend" you would keep it.

**Step 3 — smooth.** With a 3-point moving average the remaining series becomes `(12+14+13)/3 = 13.0, (14+13+12)/3 = 13.0, …` — the local jitter disappears while the level is preserved.

---

## 9. Summary paragraph

An outlier is a point that deviates so far from the rest that it looks like it came from another mechanism; it may be an error or a rare genuine event, so detection must be followed by a **justified decision** (remove, cap, transform, replace, or model separately). Detection families are statistical (z-score, IQR/boxplot), distance-based (Euclidean, kNN), density-based (DBSCAN, LOF) and model-based (Isolation Forest, One-Class SVM, autoencoders). Smoothing is the complementary operation: instead of policing individual points it reduces random fluctuation across the whole series using binning, regression, moving averages, LOWESS, median filters and clustering. Together they convert a noisy, dirty attribute into a trustworthy one — the input every later unit assumes.

---
**Next:** [Topic 4 — Data Integration](04-data-integration-schema-redundancy.md)
