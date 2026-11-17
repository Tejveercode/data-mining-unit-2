# Topic 7 — Data Transformation: Normalization & Encoding

> **LMS page:** *Chapter 2.2 — Data Transformation: Normalization, Encoding* · **CO2**

---

## 1. What data transformation is

**Definition.** Data transformation is the process of **converting data into a more suitable format** for analysis, modelling and interpretation. After cleaning and integration the data is correct but may still be unusable: attributes are on wildly different scales, categories are text, and distributions are skewed.

Transformation improves the **scale, distribution and interpretability** of the data. The two headline techniques here are **normalization** and **encoding**; concept hierarchy generation and discretization are the next topic.

---

## 2. Normalization (scaling numeric attributes)

**Definition.** Normalization transforms numeric attributes into a **standard scale without distorting differences in the values**. Most algorithms perform better when numeric data is on a similar scale.

**Why it is essential:** an attribute in rupees (10,000–10,000,000) and one in years (18–90) would otherwise be compared as if rupees mattered 100,000× more. Distance-based and gradient-based algorithms are destroyed by that.

### 2.1 Why normalization is needed

1. Attributes have **different units or measurement scales** (salary in millions, age in years).
2. A few **large-valued attributes dominate distance** calculations (k-NN, k-means, SVM).
3. **Gradient-based** algorithms need stable convergence (neural networks, logistic regression, gradient descent) — unscaled features give zig-zag, slow or divergent training.
4. **Numerical instability** arises from very wide value ranges (overflow, tiny gradients).
5. **Visualization** becomes unreadable when ranges differ by orders of magnitude.

Normalization ensures **each attribute contributes equally**.

### 2.2 The five normalization techniques

**1. Min–Max normalization** — maps values to a fixed range, usually **[0, 1]**:
```
v' = (v − min) / (max − min)
```
To map to an arbitrary range `[new_min, new_max]`:
```
v' = new_min + (v − min)·(new_max − new_min) / (max − min)
```
- **Preserves the exact distribution and relationships** (it is a linear shift+scale).
- **Sensitive to outliers** — one extreme max compresses everything else into a narrow band.
- *Worked:* values 10, 20, 30 → min 10, max 30 → 0, 0.5, 1.

**2. Z-score normalization (standardization)** — mean 0, standard deviation 1:
```
v' = (v − mean) / std_dev
```
- Best when data is roughly **normal**, or when **variance** matters.
- **Not bounded** to [0, 1]; robust-ish but the mean/σ are themselves affected by outliers (use robust scaling for that).
- *Worked:* values 10, 20, 30 → mean 20, σ = 8.165 → −1.22, 0, 1.22.

**3. Decimal scaling normalization** — move the decimal point based on the **maximum absolute value**:
```
v' = v / 10^j    where j is the smallest integer such that max|v'| < 1
```
*Example:* if the largest value is **999**, divide all values by **1000** → 0.999.
- Simple and preserves the shape of the distribution; used when consistent scaling is needed without changing distributional form.

**4. Log transformation** — reduces the effect of large values and skew:
```
v' = log(v)   (use log(1+v) when zeros exist)
```
- Best for **income, population, sales, counts** spanning several orders of magnitude.
- Compresses the right tail; makes multiplicative relationships additive.

**5. Robust scaling** — uses **median and interquartile range** instead of mean and standard deviation:
```
v' = (v − median) / IQR
```
- Best when the data **contains many outliers** that must not influence the scaling.

*(Also worth naming: **unit-vector / L2 normalization** — divide each row by its Euclidean length, standard in text mining; **power/Box–Cox transforms** to stabilise variance.)*

### 2.3 When to use which — the decision table

| Method | Formula | Use when | Watch out |
|---|---|---|---|
| **Min–Max** | `(v−min)/(max−min)` | neural networks, algorithms expecting data in [0,1]; bounded inputs needed | outliers squash the rest |
| **Z-score** | `(v−μ)/σ` | Gaussian-ish data; PCA, SVM, linear models, k-means | assumes a meaningful mean/σ |
| **Decimal scaling** | `v/10^j` | quick uniform scaling, keeps distribution shape | crude; ignores shape entirely |
| **Log** | `log(v)` | heavy-tailed/skewed data (income, counts) | undefined at 0 → use log(1+v) |
| **Robust** | `(v−median)/IQR` | many outliers present | ignores tail information deliberately |

**Leakage warning (write it once, it is a mark):** compute `min/max/mean/σ/median/IQR` on the **training set only**, then apply the same numbers to validation and test. Fitting the scaler on all data leaks information and inflates reported accuracy.

---

## 3. Encoding (converting categories to numbers)

**Definition.** Encoding transforms **categorical (non-numeric) data into numerical values** so algorithms can process it. Most algorithms require numeric input — they cannot compute a distance or a gradient on the string `"Red"`.

### 3.1 Why encoding is needed
1. Algorithms expect **numerical input**.
2. Categorical variables need a **mathematical representation**.
3. Encoding **preserves category information** for effective modelling.
4. Without it, algorithms fail or produce silent nonsense.
5. Different encoding methods represent **relationships between categories** differently — the choice changes model behaviour.

### 3.2 The six encoding techniques

**1. Label encoding (integer encoding).** Assigns a unique integer to each category: `Male = 0, Female = 1`.
- Fine for **ordinal** categories; **risky for nominal** ones because the integers imply an artificial order and magnitude (the model may infer `Blue(2) > Red(0)` and even `Blue = 2 × Red`).
- Tree-based models are less harmed (they can split on any subset), but linear models are.

**2. One-hot encoding (dummy variables).** A separate **binary column per category**, 1 if present, 0 otherwise:
```
Red   → 1 0 0
Blue  → 0 1 0
Green → 0 0 1
```
- **Prevents any implied order**; the standard for **nominal** data with a small number of categories.
- Cost: **dimensionality grows with cardinality** (a 5,000-city column becomes 5,000 columns) and sparsity increases. Drop one column (`drop_first`) to avoid perfect multicollinearity for linear models.

**3. Ordinal encoding.** Assigns numbers **respecting the natural order**:
```
High School = 1, Graduate = 2, Post Graduate = 3
```
- Correct for genuinely **ordered** categories (education, severity, satisfaction rating).

**4. Frequency encoding.** Replaces each category with **how often it occurs**: category A appearing 50 times → 50; B appearing 20 times → 20.
- Compact, works for **high-cardinality** features; loses the label identity and can collide (two equally frequent categories get the same value).

**5. Target (mean) encoding.** Replaces each category with the **average value of the target** for that category:
- Churn example: category A has 60 % churn → 0.6; B has 30 % → 0.3.
- Powerful with **boosting models** and high cardinality, but **leaks the target** unless computed with out-of-fold cross-validation and smoothing; must be fitted inside the CV loop.

**6. Binary encoding.** Convert each category to its **binary number**, then split the digits across columns. For 100 categories, label encoding needs 1 column and one-hot needs 100; binary encoding needs about `log₂(100) ≈ 7`.
- Good when the **category space is very large** and memory matters.

*(Also: **hashing trick** — hash categories into a fixed number of columns, constant memory, at the cost of collisions; **embeddings** — learned dense vectors for very high cardinality, the deep-learning answer.)*

### 3.3 Choosing the right encoding (LMS table)

| Method | Best for |
|---|---|
| **Label encoding** | **ordinal** data (order exists) |
| **One-hot encoding** | **nominal** categories with a **small** number of unique values |
| **Frequency encoding** | **large** category sets |
| **Target encoding** | **boosting** models; needs regularization/cross-validation |
| **Binary encoding** | when the **dataset size must be kept small** |

### 3.4 Problems encoding solves

- Converts categorical text into numbers a model can consume.
- Preserves category information **without bias** (one-hot avoids invented order).
- Handles **large category sets efficiently** (frequency, binary, hashing).
- Prepares data for algorithms that require numeric vectors.
- **Improves accuracy** by representing categories faithfully.

**Common mistakes to avoid:** one-hot on 10,000-category IDs (memory explosion — use target/frequency/hashing), label encoding a nominal attribute and letting a linear model treat it as numeric, and computing target encoding on the full dataset (leakage, fake accuracy).

---

## 4. Worked end-to-end mini example

Raw rows:

| Age | Salary | City | Education |
|---|---|---|---|
| 25 | 30000 | Delhi | Graduate |
| 40 | 120000 | Mumbai | Post Graduate |
| 35 | 60000 | Delhi | High School |

**Step 1 — normalize Age (min–max):** min 25, max 40 → 0, 1.0, 0.667.
**Step 2 — normalize Salary (min–max):** min 30000, max 120000 → 0, 1.0, 0.333.
**Step 3 — encode City (one-hot):** `Delhi = [1,0]`, `Mumbai = [0,1]` → rows `[1,0]`, `[0,1]`, `[1,0]`.
**Step 4 — encode Education (ordinal, order matters):** High School = 1, Graduate = 2, Post Graduate = 3 → 2, 3, 1.

Final matrix (6 numeric columns):
```
[0,    0,    1, 0, 2]
[1.0,  1.0,  0, 1, 3]
[0.667,0.333,1, 0, 1]
```
Note how each step was chosen by the **attribute type**: interval/ratio → normalization; nominal → one-hot; ordinal → ordinal encoding.

---

## 5. Summary paragraph

Data transformation puts correct data into a usable form. **Normalization** removes unit and magnitude effects so every attribute contributes fairly: min–max to [0,1] (linear, outlier-sensitive), z-score to mean 0 / sd 1 (for Gaussian or variance-sensitive methods), decimal scaling (crude uniform shift), log (for heavy tails) and robust scaling by median/IQR (when outliers must not distort the scale). **Encoding** makes categories numeric: label encoding for ordinals, one-hot for small nominal sets, ordinal encoding for real hierarchies, and frequency, target, binary or hashing encodings for high cardinality — with target encoding requiring out-of-fold computation to avoid leakage. Fit every transformation on the training data only, then apply the identical parameters to test data.

---
**Next:** [Topic 8 — Concept Hierarchy Generation & Discretization](08-concept-hierarchy-discretization.md)
