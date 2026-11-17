# Topic 8 — Data Transformation: Concept Hierarchy Generation & Discretization

> **LMS page:** *Chapter 2.2 — Data Transformation: Concept Hierarchy Generation, Discretization* · **CO2**
> *Your LMS page for this topic had not arrived when this was written, so it is built from the course textbooks (Han Ch. 3, Tan Ch. 2) in the same style and depth as the other topics. It will be aligned word-for-word with your page once it arrives.*

---

## 1. Discretization: turning continuous into categorical

**Definition.** Discretization divides the **range of a continuous attribute into intervals**; each interval is mapped to a small set of category labels. It replaces a numeric attribute by an ordinal/nominal one.

**Binarization** is the special case with exactly **two** intervals (e.g. `income > 50,000 → 1, else 0`).

**Example.** `Age` (0–100) → `{child, young, middle-aged, senior}`; `Income` (numeric) → `{low, medium, high}`.

### 1.1 Why discretize? (six reasons)

1. **Some algorithms require categorical input** — classic Apriori/association rules work on items, decision trees split on discrete tests, Naïve Bayes for nominal attributes.
2. **Interpretability** — a rule `age ∈ [25, 40] → buys laptop` is readable; `0.34 < age_scaled < 0.61` is not.
3. **Noise reduction** — small measurement jitter inside a bin disappears.
4. **Non-linear relationships** — binning lets a linear model express a stepwise, non-linear effect.
5. **Compression** — fewer distinct values = smaller, faster data structures.
6. **Robustness** — insensitive to extreme values once they fall into the same top bin.

**Costs:** information loss (values inside a bin become indistinguishable), arbitrary boundaries, and poor choices can destroy a real pattern — a boundary placed in the middle of an important range hides it.

### 1.2 Unsupervised discretization (ignores the class label)

**(a) Equal-width (equal-interval) binning.** Divide the range `[min, max]` into *k* intervals of equal width:
```
width w = (max − min) / k
```
Boundaries: `min + w, min + 2w, …, min + (k−1)w`.

*Worked example.* Values: 5, 12, 18, 25, 31, 40, 47, 55, 63, 70 with k = 3.
min = 5, max = 70 → w = (70 − 5)/3 = 21.67.
Bins: **[5, 26.67), [26.67, 48.33), [48.33, 70]** → counts 3, 3, 4.
- **Pros:** simple, fast, easy to explain.
- **Cons:** **sensitive to outliers and skewed distributions** — one huge value leaves the first bins almost empty.

**(b) Equal-frequency (equal-depth) binning.** Put the **same number of values** in each bin (use quantiles). With n = 10 and k = 3, `ceil(10/3) = 4` values per bin:
- Bins: `[5, 12, 18, 25]`, `[31, 40, 47, 55]`, `[63, 70]` → counts 4, 4, 2.
- **Pros:** handles skew well; every bin is informative.
- **Cons:** boundaries land on arbitrary values, equal values can be split across bins, and it still ignores the class.

**(c) K-means (clustering-based) discretization.** Run 1-D k-means on the attribute; cluster centres sorted → bin boundaries halfway between adjacent centres.
- Produces **natural groupings** (e.g. income clusters at 15k, 45k, 120k) rather than artificial equal ranges.

**(d) Histogram / quantile-based partitioning** — a generalisation using a histogram of the distribution; used inside data-reduction (histograms as a compact summary).

### 1.3 Supervised discretization (uses the class label — usually better)

**(a) Entropy-based (information-gain) discretization — the MDLP idea.**
Choose the split point that maximises **information gain** (minimises entropy) with respect to the class.

```
Entropy(S) = − Σ pᵢ · log₂ pᵢ
Gain(S, split) = Entropy(S) − Σ (|Sᵥ|/|S|)·Entropy(Sᵥ)
```

**Full worked example.** Data: `Age` with class `Buys_Laptop`:

| Age | 18 | 20 | 22 | 25 | 30 | 35 | 40 | 45 | 50 | 55 |
|---|---|---|---|---|---|---|---|---|---|---|
| Buys | N | N | Y | Y | Y | N | N | Y | Y | Y |

Overall: 6 Yes, 4 No → `Entropy = −0.6log₂0.6 − 0.4log₂0.4 = 0.971`.

Now evaluate every candidate cut point (always cut **between two distinct values**):

| Split | Left (Y/N) | E(left) | Right (Y/N) | E(right) | Weighted | **Gain** |
|---|---|---|---|---|---|---|
| **≤ 20** | 0/2 | 0.000 | 6/2 | 0.811 | 0.649 | **0.322** ← best |
| ≤ 22 | 1/2 | 0.918 | 5/2 | 0.863 | 0.880 | 0.091 |
| ≤ 30 | 3/2 | 0.971 | 3/2 | 0.971 | 0.971 | 0.000 |
| ≤ 40 | 3/4 | 0.985 | 3/0 | 0.000 | 0.690 | 0.281 |
| ≤ 47 | 4/4 | 1.000 | 2/0 | 0.000 | 0.800 | 0.171 |

Worked in full for the winner (**≤ 20**, i.e. threshold 21):
- Left {18, 20}: N, N → entropy = `−(2/2)log₂(2/2) = 0`
- Right {22…55}: 6Y, 2N → entropy = `−0.75log₂0.75 − 0.25log₂0.25 = 0.811`
- Weighted = `(2/10)(0) + (8/10)(0.811) = 0.649`
- **Gain = 0.971 − 0.649 = 0.322**

and for the split at **≤ 22** (the one that looks "obvious" and is worse):
- Left {18,20,22}: 1Y, 2N → 0.918 ; Right {25…55}: 5Y, 2N → 0.863
- Weighted = `(3/10)(0.918) + (7/10)(0.863) = 0.880` → **Gain = 0.091**

So the best first cut is **at age 21**; recurse on each side, stopping when the gain is negligible or the bin is too small. This is exactly how **C4.5/CART** pick numeric thresholds — the link examiners like. (The full computation is in `code/unit2_toolkit.py → best_entropy_split`, which returns threshold 21 and gain 0.322.)

**How to present this in an exam:** (1) state the base entropy, (2) show a table of candidate splits with left/right class counts, (3) compute weighted entropy and gain for the best two, (4) name the winner, (5) say the process recurses. That structure alone typically earns most of the marks.

**(b) χ²-based (ChiMerge) discretization.** Start with every distinct value in its own interval, then repeatedly merge the **adjacent pair with the lowest χ²** (most similar class distribution) until a stopping criterion is met.

**(c) CART-style binary splits** — choose the split minimising the **Gini index**:
```
Gini(S) = 1 − Σ pᵢ²
```

**(d) MDLP (Minimum Description Length Principle)** — accept a split only if the gain exceeds the cost of encoding the cut, which prevents over-splitting.

### 1.4 Top-down vs bottom-up (the classification the LMS title mentions)

| Direction | Also called | Procedure | Examples |
|---|---|---|---|
| **Top-down (splitting)** | divisive | start with **one interval containing everything**, recursively **split** at the best point | entropy/information-gain, CART, MDLP |
| **Bottom-up (merging)** | agglomerative | start with **one interval per distinct value**, repeatedly **merge** the best adjacent pair | ChiMerge, equal-frequency construction |

Both produce a set of intervals; top-down suits supervised gain-based methods, bottom-up suits χ² merging.

### 1.5 Choosing a discretization method

| Situation | Choose |
|---|---|
| Quick, explainable bins | equal-width |
| Skewed data, balanced bin sizes | equal-frequency |
| Natural groupings | k-means |
| Class labels available and accuracy matters | entropy / MDLP / ChiMerge |
| Two categories only (present/absent) | binarization with a domain threshold |

---

## 2. Concept hierarchy generation

**Definition.** A **concept hierarchy** organises the values of an attribute from **specific (low level) to general (high level)**, forming a tree. It is what lets you analyse data at multiple levels of abstraction.

**Example — location:**
```
all
 └── country (India)
      └── state (Rajasthan)
           └── city (Jaipur)
                └── street (MI Road)
```
**Example — product:**
```
all → Electronics → Computers → Laptops → Ultrabooks
```
**Example — age:** `numeric 0–100` → `{child, teenager, young adult, adult, senior}` (a discretized hierarchy).

### 2.1 Why concept hierarchies matter

1. **Multi-level analysis** — you can "roll up" (Jaipur → Rajasthan → India) or "drill down", exactly like OLAP.
2. **Generalisation** — rules can be stated at a useful level: *"most buyers from Rajasthan are young adults"* instead of 10,000 city-level rules.
3. **Data reduction** — replacing 5,000 cities with 28 states compresses the data enormously.
4. **Smaller, more meaningful itemsets** — in association mining, 200 products grouped into 12 categories makes patterns findable.
5. **Interpretability** — generalised rules are what a human decision-maker can act on.

### 2.2 How concept hierarchies are generated

**(a) Schema-based (explicit) generation.** The hierarchy is **known in advance** and declared in the schema or by the domain expert: `street < city < state < country`. The attribute values are then replaced by their higher-level labels.

**(b) Data-based (implicit) generation by value grouping.** The hierarchy is **discovered from the data** when no schema exists:
- **Partial-order / distinct-value analysis** — if a database stores both `city` and `state`, the functional dependency `city → state` reveals a level; count distinct values (5,000 cities vs 28 states) to identify which is more general.
- **Number of distinct values rule** — an attribute with many distinct values is low-level; few distinct values is high-level.
- **Semantic distance / string clustering** — values are clustered by similarity to form groups (all `*pore` cities together).
- **Binning / discretization** — numeric attributes are converted into labelled intervals, giving a numeric concept hierarchy.
- **Text clustering for documents/keywords** — high-level terms replace specific ones for text mining.

### 2.3 The two ways to specify a hierarchy in practice

| Approach | Where the knowledge comes from | Example |
|---|---|---|
| **Explicit / user-specified** | expert or schema declares the levels | `region → country → state → city` |
| **Implicit / automatic** | mined from the data distribution | clustering 5,000 cities into 30 groups by similarity; binning age |

**Trade-off:** explicit hierarchies are meaningful and reliable but need domain work; automatic ones are scalable but can produce groupings that make no business sense — always have a human review them.

---

## 3. Discretization vs concept hierarchy — how they relate

| | **Discretization** | **Concept hierarchy** |
|---|---|---|
| Input type | usually **numeric** continuous | any attribute, including nominal (city, product) |
| Output | a set of **intervals / bins** | a **tree of levels** from specific to general |
| Levels | one level (though recursive splitting gives several) | multiple levels by construction |
| Purpose | make numeric data usable for categorical algorithms | enable multi-level (roll-up/drill-down) analysis |
| Mechanism | split range | group values into increasingly general concepts |

**In one sentence:** discretization creates **one level** of categories from a continuous range; concept hierarchy generation builds the **ladder** of levels (and discretization of a numeric attribute is one way to build a level of that ladder).

---

## 4. Worked end-to-end example

Raw attribute: `Age` = 23, 27, 34, 41, 45, 52, 58, 64, 71, 19.

1. **Discretize (equal-width, k = 4):** min 19, max 71 → w = 13 → bins **[19,32), [32,45), [45,58), [58,71]** → labels `Young (19–32)`, `Adult (32–45)`, `Middle (45–58)`, `Senior (58–71)`.
2. **Build a hierarchy:** `Age (numeric) → age-band (4 labels) → is_senior (yes/no)`.
3. **Use it:** mining at the band level gives general rules; drilling down into exact ages gives detail — and the item count for association mining drops from 53 distinct ages to 4 labels.

---

## 5. Summary paragraph

Discretization replaces a continuous attribute by intervals, making numeric data usable for categorical algorithms and interpretable for humans. **Unsupervised** methods (equal-width, equal-frequency, k-means) ignore the class and are fast but arbitrary; **supervised** methods (entropy/information gain, χ²/ChiMerge, CART/Gini, MDLP) choose boundaries that separate classes and are usually more accurate. Top-down methods split one interval repeatedly; bottom-up methods merge fine intervals. **Concept hierarchies** generalise values from specific to general (city → state → country; product → category), either declared from the schema or mined from the data, enabling roll-up/drill-down analysis, generalised rules and large data reduction. Discretization builds one level; a hierarchy builds the ladder.

---
**Next:** [Topic 9 — Introduction to Frequent Pattern Mining (Support, Confidence, Lift)](09-frequent-pattern-mining-basics.md)
