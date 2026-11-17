# Topic 9 — Introduction to Frequent Pattern Mining; Support, Confidence, Lift

> **LMS pages:** *Chapter 2.2 — Introduction to Frequent Pattern Mining* (**CO2**) and *Chapter 2.2 — Frequent Itemset Mining Concepts: Support, Confidence, Lift* (**CO3**)
> Both pages are covered in full below, in their own order, with the worked examples from your pages completed.

---

# PART A — Introduction to Frequent Pattern Mining

## A1. What frequent pattern mining is

**Definition.** Frequent pattern mining is one of the **core tasks of data mining**. It focuses on discovering **patterns, relationships or associations among items in large datasets**. A **frequent pattern** is a **set of items, subsequences or substructures that appear together frequently in a dataset**.

It is the foundation of **market basket analysis, recommendation systems, web usage mining and bioinformatics**.

**What counts as a "frequent pattern"?** Any pattern **whose frequency of occurrence is higher than a user-defined threshold** (the minimum support). The threshold decides everything: the same data yields different pattern sets at different thresholds.

**Examples of patterns:**
- pairs of products frequently bought together (itemsets),
- sequences of web-page visits (sequences),
- common substructures in chemical compounds (substructures).

## A2. Key terms (the definitions your page lists — learn them verbatim)

| Term | Definition |
|---|---|
| **Support** | how often a set of items appears in the dataset; the **strength** of the pattern in the whole collection |
| **Itemset** | a collection of one or more items (e.g. *Bread and Butter* is a **two-itemset**) |
| **Frequent itemset** | an itemset whose support is **greater than or equal to** the minimum support threshold |
| **Candidate itemset** | a **potential** itemset that may become frequent and still needs to be evaluated |
| **Transaction** | a record containing a set of items purchased or occurring together |
| **Minimum support** | the **user-defined value** that determines whether an itemset is frequent |

Two more that the later pages add: **association rule** (`X → Y`, where X and Y are disjoint) and **minimum confidence** (the threshold a rule's confidence must reach).

> **Why "candidate" matters.** Candidate itemsets are the *output of the join step and the input to counting* — they are the reason Apriori is expensive, and the thing FP-Growth eliminates. If an exam asks "what does FP-Growth avoid generating?", the answer is **candidate itemsets**.

## A3. Why frequent pattern mining is important

It reveals **co-occurrence relationships** — which items, events or behaviours appear together. Those relationships support business decisions, improve customer experience and enhance system intelligence.

| Use | What it does |
|---|---|
| **Market basket analysis** | identifies which items customers often buy together |
| **Recommendation systems** | recommends complementary products based on buying behaviour |
| **Fraud detection** | finds unusual combinations of events that indicate suspicious activity |
| **Scientific research** | finds frequent patterns in genomic sequences or chemical structures |
| **Web usage mining** | understands user navigation behaviour on websites |

## A4. Types of patterns found (five types — a very likely short question)

1. **Frequent itemsets** — sets of items appearing frequently in transactions (e.g. *Milk, Bread*).
2. **Frequent sequences** — ordered lists occurring in a specific order (e.g. a user viewing Page A → Page B → Page C).
3. **Frequent substructures** — patterns in graphs or networks (protein structures, social-network patterns).
4. **Closed frequent itemsets** — frequent itemsets that have **no superset with the same support count**.
5. **Maximal frequent itemsets** — frequent itemsets that have **no frequent superset at all**.

*Each type provides different insights depending on the application.* The last two are **compact representations**: closed sets preserve all support information in fewer itemsets; maximal sets are the most compact but lose subset supports.

*Example showing the difference:* if `{A,B}` has support 3 and `{A,B,C}` also has support 3, then `{A,B}` is **not closed** (a superset has the same support), while `{A,B,C}` is both **closed and maximal**.

## A5. Challenges in frequent pattern mining

| Challenge | Why it is hard |
|---|---|
| **Large number of possible itemsets** | with n items there are **2ⁿ** possible itemsets — the search space grows exponentially |
| **Low minimum support** | a small threshold produces a very large number of frequent patterns, making processing difficult |
| **Data sparsity** | datasets with many unique items have low overlap, making pattern extraction hard |
| **Multiple scans of data** | some algorithms (Apriori) must scan the database many times, increasing cost |
| **Memory limitations** | storing and processing millions of candidate itemsets needs significant memory |

**These five challenges are exactly the design goals of the algorithms** — which is the best possible exam link to make.

## A6. Popular algorithms (three names, one line each)

| Algorithm | Strategy |
|---|---|
| **Apriori** | **bottom-up**; generates candidate itemsets and tests their support; based on the principle that all subsets of a frequent itemset must also be frequent |
| **FP-Growth** | uses a **compressed representation (FP-Tree)**; **avoids candidate generation**; much faster than Apriori on large datasets |
| **Eclat** | **depth-first search** with a **vertical data representation** (item → list of transaction ids); efficient for **dense** datasets |

> **Eclat in one sentence for the exam:** instead of storing which items each transaction contains, Eclat stores **which transactions each item occurs in** (a vertical/tid-list format), then intersects those tid-lists to get the support of an itemset — no repeated database scans, and the intersection is fast set arithmetic.

**Why a vertical format helps:** support of `{A,B}` = `|tid(A) ∩ tid(B)|`. The intersection gives the *exact* count instantly and produces the tid-list for the larger itemset as a by-product, which is why Eclat suits **dense** data (many long transactions).

## A7. Applications across industries

| Sector | Use |
|---|---|
| **Retail & e-commerce** | market basket analysis, store-layout design, cross-selling, promotions |
| **Banking** | fraud detection, credit-risk analysis |
| **Telecommunications** | churn prediction, network optimisation |
| **Healthcare** | co-occurring disease symptoms, treatment combinations |
| **Social media** | trending topics, common user behaviours |
| **Manufacturing** | predicting equipment failures from frequent fault patterns |

## A8. The importance of the support threshold

- **Too high** → important but **rare** patterns are missed (e.g. the fraud combination you were looking for).
- **Too low** → **too many patterns** are generated, making analysis difficult (and mining slow).

The threshold must **balance meaningful pattern discovery against computational efficiency**. In practice: start high, inspect the output, lower it until the pattern count becomes unmanageable — and remember that *rare but valuable* patterns are exactly what "too high" destroys.

---

# PART B — Frequent Itemset Mining: Support, Confidence, Lift

## B1. Introduction

Frequent itemset mining identifies **sets of items that appear together frequently** in transactional datasets. It is used mainly in **market basket analysis, recommendation systems, fraud detection and behavioural analytics**.

**Association rule mining is built on top of frequent itemset mining** and uses three measures — **support, confidence, lift** — which determine how **strong and meaningful** the discovered patterns are.

## B2. Transactions and itemsets

A **transaction** is a collection of items purchased or appearing together; an **itemset** is a set of one or more items.

**Your page's example dataset:**

| TID | Items |
|---|---|
| T1 | Milk, Bread, Eggs |
| T2 | Milk, Diaper |
| T3 | Bread, Butter, Milk |
| T4 | Bread, Diaper, Eggs |

The goal: **find which item combinations occur frequently.**

## B3. Support

**Support of an itemset X = (number of transactions containing X) / (total number of transactions).**

Support ranges from **0 to 1**. A higher support means the itemset is **common** and may be useful for **general** patterns.

**Example (your page):** if `{Milk, Bread}` appears in **3 out of 10** transactions, `support = 3/10 = 0.3`.

**Using your four-transaction dataset (N = 4):**
```
support({Milk})        = 3/4 = 0.75     (T1, T2, T3)
support({Bread})       = 3/4 = 0.75     (T1, T3, T4)
support({Eggs})        = 2/4 = 0.50     (T1, T4)
support({Diaper})      = 2/4 = 0.50     (T2, T4)
support({Milk, Bread}) = 2/4 = 0.50     (T1, T3)
```

**Why support matters (five reasons from your page):**
1. It identifies **how frequently items occur together**.
2. It helps **remove rare combinations** that may not be meaningful.
3. It **controls the size of the output** by setting a minimum support threshold.
4. It ensures discovered patterns are **statistically significant**.
5. It **improves efficiency** by ignoring itemsets that appear too rarely.

*A rule with high support is more useful for general business decisions.*

## B4. Confidence

**Confidence measures the strength of an association rule** — how often the consequent appears in transactions that contain the antecedent.

```
For X → Y:   confidence = support(X ∪ Y) / support(X)
```
It is the **conditional probability that Y occurs given that X has already occurred**.

**Example (your page):** if **100 customers bought Milk** and **60 of those also bought Bread**, then `confidence(Milk → Bread) = 60/100 = 0.6` — *60 % of customers who buy Milk also buy Bread.*

**Using the four-transaction dataset:**
```
confidence(Milk → Bread) = 0.50 / 0.75 = 0.667   (66.7 %)
confidence(Bread → Milk) = 0.50 / 0.75 = 0.667
```
Confidence is **directional**: with different supports, `X → Y` and `Y → X` differ. (Here the supports coincide, so both are 0.667 — state that, it shows you understand why.)

**Why confidence matters:**
1. It tells **how reliably the rule predicts the consequent**.
2. High-confidence rules are more useful for **recommendation systems**.
3. It helps determine **purchasing-behaviour patterns**.
4. It is used to **filter out weak or unreliable rules**.
5. A rule with **high support but low confidence may still not be useful**, because it does not strongly indicate a relationship.

## B5. Lift

**Lift evaluates the usefulness or significance of a rule**: it compares the **observed** support of X and Y together with the support **expected if X and Y were independent**.

```
lift(X → Y) = support(X ∪ Y) / (support(X) × support(Y))
```

| Lift | Interpretation |
|---|---|
| **= 1** | X and Y occur **independently** |
| **> 1** | **positive association** — X increases the likelihood of Y; a strong, useful rule |
| **< 1** | **negative association** — X decreases the likelihood of Y; the rule is not meaningful (they are substitutes/competitors) |

**Your page's example:** if Milk and Bread appear together **more often than expected** from their individual supports, lift > 1.

**Using the four-transaction dataset:**
```
lift(Milk → Bread) = 0.50 / (0.75 × 0.75) = 0.50 / 0.5625 = 0.889
```
Lift **below 1** → although confidence was a respectable 66.7 %, milk and bread are in fact **slightly negatively associated** in this tiny dataset. *This is the single most important lesson of the topic: confidence is not enough.*

## B6. Why lift is important (it fixes what confidence cannot)

**Confidence may be high simply because the consequent item is very frequent.** Lift corrects for that by dividing by the consequent's own base rate.

Lift is important because:
1. It identifies **true associations**, not just popular items.
2. It helps avoid **misleading rules caused by high-frequency items**.
3. It measures **how much better than random chance** the rule performs.
4. It helps **select the most meaningful rules** for decision-making.

*A high lift indicates a strong, meaningful relationship useful for recommendations and marketing.*

## B7. The 100-transaction worked example (your page, expanded)

**Assume 100 total transactions.**
```
support(Milk)        = 0.5
support(Bread)       = 0.4
support(Milk, Bread) = 0.3
```

**Confidence:**
```
confidence(Milk → Bread) = 0.3 / 0.5 = 0.6    (60 %)
confidence(Bread → Milk) = 0.3 / 0.4 = 0.75   (75 %)
```

**Lift (identical in both directions — lift is symmetric):**
```
lift = 0.3 / (0.5 × 0.4) = 0.3 / 0.2 = 1.5
```

**Interpretation (write exactly this):** lift = 1.5 > 1 means Milk and Bread are bought together **more often than expected** under independence → a **positive, strong association**. Note that the two rules have **different confidence (0.6 vs 0.75) but the same lift (1.5)** — confidence is directional, lift is symmetric. That single sentence answers many questions.

## B8. Differences between the three measures (your page's summary table)

| Measure | What it measures | What it shows |
|---|---|---|
| **Support** | **frequency** | how common the itemset is |
| **Confidence** | **rule strength** | how often Y appears when X appears |
| **Lift** | **rule significance** | how much better the rule is than random chance |

*Together, these three determine whether a rule is **frequent, strong and statistically interesting**.*

**The one-line memory hook:** **S**upport = *how often*; **C**onfidence = *how reliably*; **L**ift = *how much better than chance*.

---

## B9. Summary paragraph

Frequent pattern mining finds itemsets, sequences and substructures that occur more often than a user-set threshold, and it is the base of market basket analysis, recommendation, fraud detection and web mining. Its key terms are support, itemset, frequent itemset, candidate itemset, transaction and minimum support; its five challenges (2ⁿ itemsets, low support, sparsity, repeated scans, memory) are exactly why the three algorithms exist — **Apriori** (bottom-up candidates + pruning), **FP-Growth** (two scans + compressed FP-tree, no candidates) and **Eclat** (depth-first vertical tid-list intersections, good on dense data). Within that, support measures frequency, confidence measures `P(Y|X)` and lift divides confidence by Y's base rate, so that lift = 1 is independence, > 1 positive and < 1 negative — the measure that catches rules which are merely popular rather than genuinely associated.

---
**Next:** [Topic 10 — Apriori Algorithm: Working Principle](10-apriori-working-principle.md)
