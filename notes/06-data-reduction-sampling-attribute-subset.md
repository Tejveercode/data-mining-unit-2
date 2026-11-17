# Topic 6 — Data Reduction: Sampling & Attribute Subset Selection

> **LMS page:** *Chapter 2.2 — Data Reduction: Sampling, Attribute Subset Selection* · **CO2**

---

## 1. Why these two techniques

Data reduction shrinks a dataset in two different directions: **sampling reduces the number of rows**, **attribute subset selection reduces the number of columns**. Large datasets slow processing, raise storage cost and make training inefficient; both techniques keep the analytical value while cutting the cost.

---

## 2. Sampling

**Definition.** Sampling is the process of **selecting a representative subset of the data** instead of using the entire dataset. A smaller sample can be analysed or used to train a model **provided it accurately represents the full dataset**.

**Two properties decide whether a sample is any good:**
- **Representativeness** — the sample has the same structure as the population (same class proportions, same distribution). A biased sample is worse than no sample.
- **Adequate size** — large enough that random variation is small.

### 2.1 When sampling is used

- The dataset is **too large to process in memory**.
- A **quick approximation** is needed for preliminary analysis (profiling, EDA).
- The algorithm has **very high computational cost** (SVM, deep learning, k-NN).
- **Real-time decisions** require faster processing.
- The data is a **stream** whose length is unknown.

### 2.2 Types of sampling (five required, plus extras for depth)

**1. Random (simple random) sampling.** Each record has an **equal probability** of selection; avoids bias and needs no prior knowledge of the distribution.
- **Without replacement (SRSWOR)** — a record can be chosen once (the standard).
- **With replacement (SRSWR)** — records may repeat; the basis of **bootstrap** resampling, used to estimate model variance (and of bagging).

**2. Stratified sampling.** The dataset is divided into meaningful groups called **strata** (e.g. class label, region, income band), and samples are drawn **from each stratum proportionally**.
- Used when data contains **unbalanced categories**, to ensure each class is properly represented.
- **Guarantees** rare but important groups appear; gives **lower variance** than plain random sampling.

**3. Systematic sampling.** Choose a **random start**, then select **every k-th record** (`k = N/n`).
- Useful for ordered datasets and cheap to implement.
- **Danger:** if the data has a **periodicity matching k** (every 7th record is a Sunday), the sample becomes biased.

**4. Cluster sampling.** Data is divided into **clusters** (stores, regions, schools, blocks); **entire clusters** are selected at random and every record inside is studied.
- Used when data is **naturally grouped** or field collection is geographically expensive.
- Cheaper, but less precise than random sampling for the same n, because records inside a cluster are similar to each other.

**5. Reservoir sampling.** For **streaming data** where the number of records is unknown: maintain a fixed-size reservoir; for the *i*-th record, keep it with probability `k/i`, replacing a random existing element.
- One pass, uniform sample, O(k) memory — the standard algorithm for streams.

**Additional methods worth naming:** **multistage sampling** (cities → districts → households), **progressive/adaptive sampling** (start small, add data while accuracy improves), **importance sampling** (oversample informative cases), **negation/undersampling** (keep all positives, sample negatives — for imbalance).

### 2.3 Advantages of sampling

- **Reduces computation time** significantly.
- Enables processing of datasets **too large to fit in memory**.
- Makes **exploratory data analysis faster**.
- Useful for **real-time analysis** when full data access is impossible.
- **Preserves essential trends and patterns** when done correctly.

### 2.4 Limitations of sampling

- If the sample is **not representative**, the analysis is **misleading**.
- **Rare events may be missed** in small samples (a 0.1 % fraud class can vanish).
- **Bias** arises if sampling is done incorrectly (convenience samples, periodicity, non-response).
- It **cannot fully replace detailed analysis** when exact accuracy is critical (audits, billing).

### 2.5 Sample size — the two formulas you may be asked to use

**For a mean:**
```
n = (Z·σ / E)²
```
Z = 1.96 at 95 % confidence, σ = population standard deviation, E = tolerated error.
*Example:* σ = 10 marks, E = 1 mark → n = (1.96×10/1)² = 384.16 → **385**.

**For a proportion:**
```
n = Z²·p(1−p) / E²
```
Use `p = 0.5` when unknown — it gives the maximum (safest) n.
*Example:* E = 0.03, 95 % confidence → n = 3.8416 × 0.25 / 0.0009 = **1068**.

**Finite population correction** (when the sample is a large share of the population):
```
n_adj = n / (1 + (n − 1)/N)
```

**Standard error of the mean:** `SE = σ/√n`. Quadrupling n only halves the error — the reason gigantic samples are not worth the cost.

**Sampling error vs non-sampling error.** *Sampling error* comes from looking at a subset; it is predictable and shrinks as n grows. *Non-sampling error* comes from bad measurement, non-response or a wrong sampling frame; it **does not shrink with n**. Write this distinction — it earns marks.

### 2.6 LMS example

A retail dataset with **1,000,000 records and 50 attributes**: a **5 % random sample** (50,000 records) is used for initial exploration — 20× less data, same conclusions about coarse trends.

---

## 3. Attribute subset selection (feature selection)

**Definition.** Attribute subset selection — usually called **feature selection** — is the process of **identifying and keeping only the most relevant attributes**, removing redundant or irrelevant ones. It reduces dimensionality and improves algorithm performance.

High-dimensional datasets contain many unimportant features that add no predictive value and can even **reduce** accuracy; subset selection simplifies the data and focuses it on the attributes that carry information.

### 3.1 Why it is needed

1. More attributes → **more model complexity and training time**.
2. Irrelevant/redundant features cause **overfitting**.
3. **Visualization** becomes impossible with too many dimensions.
4. Removing unnecessary features **improves accuracy and interpretability**.
5. It **reduces noise**, so patterns become clearer.
6. It **decreases storage and processing** requirements.

### 3.2 The three approaches (the comparison table examiners want)

| | **Filter** | **Wrapper** | **Embedded** |
|---|---|---|---|
| How it judges a feature | statistical property (correlation, χ², mutual information, variance, ANOVA F) | trains a model on each candidate subset and measures its accuracy | selection happens **during** model training |
| Uses a learning model? | **No** | **Yes, repeatedly** | Yes, once |
| Speed | **Fast** | Very slow (exponential-ish search) | Medium |
| Accuracy of the chosen subset | Good, but ignores feature interactions | **Highest** | High |
| Risk | may drop features useful only in combination | overfits the selection; expensive | tied to the chosen algorithm |
| Examples | correlation, χ², mutual information, variance threshold, ANOVA F-test | forward selection, backward elimination, RFE | **Lasso (L1)**, decision-tree/random-forest importance |

**Filter — advantages:** fast and simple, model-independent (the same subset works for any algorithm). **Disadvantages:** ignores interactions between features and with the model.

**Wrapper — advantages:** produces highly accurate feature sets because it optimises the metric you actually care about. **Disadvantages:** very slow and computationally expensive; needs nested cross-validation to avoid optimistic bias.

**Embedded — advantages:** more efficient than wrappers and still model-driven (Lasso drives useless coefficients exactly to zero; trees rank by impurity reduction). **Disadvantages:** depends heavily on the chosen algorithm.

### 3.3 Search strategies (how the subset is found)

Trying all `2^d` subsets is impossible in practice (d = 30 → over a billion).

| Strategy | Procedure | Good when |
|---|---|---|
| **Brute force** | evaluate every subset | only tiny d (the baseline showing why it is infeasible) |
| **Forward selection** | start with **no** attributes, repeatedly add the attribute that improves the score the most; stop when nothing improves | the best subset is small |
| **Backward elimination** | start with **all** attributes, repeatedly remove the one whose removal hurts least | most attributes are useful |
| **Stepwise (bidirectional)** | alternate adding and removing, allowing swaps | the practical default |
| **Recursive Feature Elimination (RFE)** | fit the model, drop the weakest feature, refit, repeat until the target count | model-driven ranking matters |

**Forward selection, step by step:**
```
S = {}                                   # chosen set
repeat:
    for each attribute a not in S:  score(S ∪ {a})
    a* = the attribute with the best score
    if score(S ∪ {a*}) > score(S):  S = S ∪ {a*}
    else: stop
```

**The known weaknesses of greedy search (state them for full marks):** forward selection never removes an attribute chosen early, backward elimination never re-adds one removed early (both get trapped), and one-at-a-time selection **fails on XOR-like problems** where two attributes are useful only together. Stepwise/floating search and wrapper-friendly models mitigate this.

### 3.4 The practical process

1. Identify **redundant features** carrying the same information (`height_cm` and `height_m`).
2. Remove **irrelevant attributes** that do not relate to the target (`phone_number` when predicting purchase behaviour).
3. **Evaluate the importance** of each attribute (correlation, mutual information, model importance).
4. **Select the subset** that maximises accuracy or interpretability.

### 3.5 Benefits

- **Reduces dimensionality** and simplifies datasets.
- **Improves model performance** by eliminating noise.
- **Reduces overfitting** (fewer attributes → lower model complexity).
- **Shortens training and prediction time**.
- **Enhances visualization and interpretability**.
- Shows **which attributes truly matter** for decision-making — often the most valuable output for a business.

> **Attribute subset selection vs dimensionality reduction (feature extraction):** subset selection **keeps the original attributes** (so meaning is preserved); extraction **creates new ones** (PCA components) that are more compact but harder to explain. Choose selection when the model must be explained to a human, extraction when attributes are many and highly correlated.

---

## 4. LMS worked example, completed

A retail dataset: **1,000,000 records × 50 attributes.**

1. **Sampling** — take a 5 % **random** (or **stratified**, if the classes are unbalanced) sample: 50,000 records. Result: exploration that took hours now takes minutes; the class proportions are preserved.
2. **Attribute subset selection** — of the 50 attributes, 15 are identified as redundant (e.g. `price_inr` and `price_usd`) or irrelevant (e.g. `customer_phone`). The remaining **35** are used for model building.
3. **Result** — data volume down 20× and width down 30 %, with accuracy maintained or improved and training time sharply reduced.

---

## 5. Summary paragraph

Sampling reduces **records**: random (equal probability), stratified (proportional within groups, lower variance, protects rare classes), systematic (every k-th, cheap but vulnerable to periodicity), cluster (whole groups, cheap but less precise), and reservoir (fixed-size, one pass, for streams) — with sample size set from `n = (Zσ/E)²` or `n = Z²p(1−p)/E²`. Attribute subset selection reduces **columns** by keeping the most relevant original attributes, using **filters** (fast, statistical, model-free), **wrappers** (accurate but slow: forward selection, backward elimination, RFE) or **embedded** methods (selection inside training: Lasso, tree importance). Both lower cost, reduce overfitting and improve interpretability — and both must be fitted **inside** cross-validation to avoid leakage.

---
**Next:** [Topic 7 — Data Transformation: Normalization & Encoding](07-data-transformation-normalization-encoding.md)
