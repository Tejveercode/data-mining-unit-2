# Topic 5 — Data Reduction: Data Cube Aggregation & Dimensionality Reduction

> **LMS page:** *Chapter 2.1 — Data Reduction: Data Cube Aggregation, Dimensional Reduction* · **CO2**

---

## 1. What data reduction is

**Definition.** Data reduction is a pre-processing technique that **reduces the size or complexity of a dataset while preserving its essential patterns and information**.

Large datasets increase computation time, memory requirements and model-training cost. Reduction produces a **compact representation** that is mined faster without significant loss of accuracy.

**Four families of data reduction** (learn this table — it organises the topic and the next topic too):

| Family | What it shrinks | Techniques | Covered in |
|---|---|---|---|
| **Data cube aggregation** | rows → summaries | roll-up, materialized views | this topic |
| **Dimensionality reduction** | columns | feature selection, feature extraction (PCA, SVD, LDA) | this topic |
| **Numerosity reduction** | rows | sampling, histograms, clustering, parametric models | Topic 6 |
| **Data compression** | the data itself | lossless/lossy encoding (wavelets, SVD) | this topic |

**A useful formula for the exam:** *data reduction = fewer rows + fewer columns + simpler values, with the mining result approximately unchanged.*

---

## 2. Data cube aggregation

**Definition.** Data cube aggregation summarises detailed data into **higher-level forms** in data warehouses and OLAP systems. A **data cube** is a multidimensional structure that stores data along multiple **dimensions** — time, location, product, customer — with **measures/facts** (sales, profit, quantity) at each cell.

**Aggregation means moving from lower-level (detailed) granularity to higher-level (summarised) granularity.**

**Examples.**
- Daily sales → weekly → monthly → quarterly → yearly sales.
- State-level sales → region-level → national-level sales.
- Per-customer transactions → per-customer monthly totals.
- Store–product–day → product–month.

### 2.1 Purpose (five reasons)

1. **Reduces data volume** — stores summarised values instead of detailed records.
2. **Improves query performance** in analytical systems (fewer rows to scan).
3. Lets users view data at **different levels of granularity**.
4. Supports **fast exploration** of trends, patterns and business summaries.
5. Provides a **compact representation while retaining essential analytical information**.

### 2.2 Levels of aggregation in a data cube

| Level | Contents | Example |
|---|---|---|
| **Base level** | most detailed / raw data | sales per product per day per store |
| **Intermediate levels** | aggregated at some dimension combinations | sales per product per month; sales per store per quarter |
| **Apex level (top)** | highest summarisation — one value for all dimensions | total annual sales for the whole company |

Data size falls sharply from base to apex; **each level is called a cuboid**, and the set of all cuboids for all dimension subsets is the **lattice** (`2^d` cuboids for d dimensions, minus the "none" cell). The **`all` (apex) value** is the grand total.

### 2.3 How data cube aggregation works (five steps)

1. **Identify the dimensions** to include (time, product, location, customer…).
2. **Define the measures** to aggregate (sales, profit, quantity, count).
3. **Apply aggregation functions** — `SUM, AVG, COUNT, MAX, MIN` (and `DISTINCT COUNT`, which is *not* additive — a classic gotcha: you cannot sum distinct customers across months).
4. **Generate the aggregated tables** (cuboids) for the required dimension combinations.
5. **Store / materialise** the commonly used aggregate views to speed up queries.

The result is a hierarchy in which users **drill down** to detail or **roll up** to summaries.

### 2.4 OLAP operations that rest on aggregation

| Operation | Meaning | Example |
|---|---|---|
| **Roll-up** (drill-up) | move to a **higher** level of aggregation, or drop a dimension | city → state → country |
| **Drill-down** (roll-down) | move to **finer** detail | year → quarter → month |
| **Slice** | fix **one** dimension, take a sub-cube | sales where `Quarter = Q1` |
| **Dice** | fix **two or more** dimensions (a sub-cube range) | `Q1–Q2` and `North–South` |
| **Pivot (rotate)** | rotate the cube to change the viewing axes | products on rows instead of columns |

### 2.5 Advantages

- Reduces the **total amount of data** to process.
- **Improves query response time** (pre-computed summaries).
- **Simplifies analysis** by providing already-summarised information.
- Supports **OLAP operations** (roll-up, drill-down, slice, dice, pivot).
- Helps in **trend analysis** and business decision-making.

**Costs to mention for full marks:** aggregation **loses detail** (you cannot recover the individual transactions), can **hide outliers** (a spike averaged away), materialized views consume **storage**, and the cube must be **refreshed** when base data changes.

---

## 3. Dimensionality reduction

**Definition.** Dimensionality reduction **reduces the number of attributes or features** in a dataset while preserving the significant information.

High-dimensional data increases complexity, slows algorithms down, and causes overfitting. Reduction simplifies the dataset and improves model performance.

### 3.1 Why it is needed (five reasons)

1. High-dimensional data causes the **curse of dimensionality**, making distance-based methods ineffective.
2. Models become prone to **overfitting** when there are many irrelevant attributes.
3. **Visualization** is impossible beyond 2–3 dimensions without projection.
4. **Speed and storage**: fewer attributes → less computation and memory.
5. It removes **irrelevant, noisy or redundant** features, which improves accuracy.

**The curse of dimensionality in one paragraph (write this).** As the number of dimensions grows, the volume of the space grows exponentially, so a fixed number of points becomes sparse. Two consequences: (i) the distance to the nearest neighbour and the distance to the farthest neighbour become almost equal, so "nearest" loses meaning and k-NN/k-means/DBSCAN degrade; (ii) with many attributes, some combination can separate any labels by chance, so a model can fit noise. Hence: reduce dimensions *before* mining.

### 3.2 The two types (the most-asked distinction)

| | **Feature selection** | **Feature extraction** |
|---|---|---|
| What it does | **selects a subset of the original attributes** | **transforms** existing features into a **new, smaller set** |
| Are new features created? | **No** | **Yes** (combinations/projections) |
| Meaning preserved? | **Yes** — the original meaning stays intact | No — a component is a blend of several attributes |
| Examples | filter, wrapper, embedded methods | PCA, SVD, LDA, autoencoders |
| Best when | interpretability matters (medical, legal, credit) | attributes are highly correlated measurements |

### 3.3 Feature selection methods

| Method | How it works | Examples |
|---|---|---|
| **Filter** | statistical tests, **no learning algorithm involved** | correlation, χ², mutual information, ANOVA F-test, variance threshold |
| **Wrapper** | trains a model **repeatedly** on candidate subsets, keeps the best-scoring subset | recursive feature elimination (RFE), forward selection, backward elimination |
| **Embedded** | selection happens **during model training** | Lasso (L1) regression, decision-tree importance, random-forest ranking |

Feature selection **reduces the number of inputs while keeping the original meanings of the attributes intact**.

### 3.4 Feature extraction methods

**Principal Component Analysis (PCA).** Transforms data into a smaller number of **components** that capture **maximum variance**. Each component is a **linear combination** of the original attributes, and components are **orthogonal (uncorrelated)**.

*Working (five steps):* standardize → covariance matrix → eigenvalues/eigenvectors → sort and keep the top *k* → project the data. Variance explained by component *i* is `λᵢ / Σλ`.

*Example (LMS):* a dataset with **50 attributes**, many correlated, can be reduced to **5–10 principal components** that still preserve most of the variance — a large cut in size with a small loss of information.

**Singular Value Decomposition (SVD).** Factorises the data matrix `X = U·Σ·Vᵗ`; keeping the top *k* singular values gives the **best possible low-rank approximation** (Eckart–Young). Used for latent semantic analysis in text, recommenders, compression, noise removal. **PCA and SVD are the same computation** — PCA is the statistical description, SVD the numerical engine.

**Linear Discriminant Analysis (LDA).** **Supervised** dimensionality reduction: finds directions that maximise **between-class separation** while minimising **within-class spread**. At most `C − 1` components for `C` classes. Often better than PCA for classification because it uses the labels.

**Autoencoders.** Neural networks with a narrow **bottleneck** layer: the encoder compresses, the decoder reconstructs, and the bottleneck becomes the reduced representation. Non-linear, powerful, but needs data and compute — the modern successor to PCA.

**Also worth naming:** wavelet transform (multi-scale compression, good for images/signals), random projection (Johnson–Lindenstrauss: preserves distances cheaply), t-SNE/UMAP (non-linear, for *visualization*, not for feeding a classifier), ICA (independent components).

### 3.5 Advantages of dimensionality reduction

- Reduces **computation time and memory** usage.
- Eliminates **multicollinearity** and irrelevant variables.
- **Enhances model performance** and reduces overfitting.
- **Improves visualization** (project to 2–3 dimensions).
- Helps reveal **hidden structures** or patterns in the data.

**Caveats:** PCA is **linear and unsupervised** (it can discard the direction that separates classes); extracted components **lose interpretability**; scaling must be done first (otherwise the largest-unit attribute dominates); and reduction fitted on the full dataset leaks test information.

---

## 4. Worked comparison — choosing between the two headline methods

| Question | Data cube aggregation | Dimensionality reduction |
|---|---|---|
| Shrinks | rows (records) | columns (attributes) |
| Operation | summary (`SUM`, `AVG`, `COUNT`) | selection or projection |
| Information lost | detail, granularity | variance/information in dropped directions |
| Typical tool | data warehouse / OLAP | preprocessing library (PCA, RFE) |
| Reversible? | No | No (projection is lossy) |
| Best for | reporting, trend analysis, dashboards | modelling, distance-based algorithms, visualization |

---

## 5. Summary paragraph

Data reduction makes a dataset smaller without changing what it says. **Data cube aggregation** shrinks rows by summarising along dimensions through base → intermediate → apex levels, enabling OLAP roll-up, drill-down, slice, dice and pivot; it speeds analytics but loses detail and can hide outliers. **Dimensionality reduction** shrinks columns, either by **feature selection** (keep a subset of the original attributes — filter, wrapper, embedded) or **feature extraction** (create new combined attributes — PCA, SVD, LDA, autoencoders), defeating the curse of dimensionality, overfitting and slow training. Aggregation changes the *granularity of records*; dimensionality reduction changes the *width of the record* — together they are how large data becomes minable.

---
**Next:** [Topic 6 — Data Reduction: Sampling & Attribute Subset Selection](06-data-reduction-sampling-attribute-subset.md)
