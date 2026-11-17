# Topic 9 — Introduction to Frequent Pattern Mining (Support, Confidence, Lift)

> **LMS pages:** *Chapter 2.2 — Introduction to Frequent Pattern Mining* and *Frequent Itemset Mining Concepts: Support, Confidence, Lift* · Course outcome **CO3: characterize the kinds of patterns that can be discovered by association rule mining.**
> *These two pages had not arrived when this was written, so it is built from the course textbooks (Han Ch. 6, Tan Ch. 6) in the same style. It will be aligned with your pages when they arrive.*

---

## 1. What frequent pattern mining is

**Definition.** Frequent pattern mining finds **patterns (itemsets, subsequences, substructures) that appear frequently in a dataset** — and, from them, **association rules** describing how items co-occur.

The canonical example is **market basket analysis**: each transaction is the set of items in one basket; the question is *"which items are bought together?"* — the engine behind "customers who bought X also bought Y".

**Why it matters (applications):**
- **Retail / e-commerce**: cross-selling, product placement, bundle design, recommendations.
- **Web usage mining**: which pages are visited together → site redesign, ads.
- **Medical**: symptom/drug co-occurrence → diagnosis and adverse-reaction signals.
- **Bioinformatics**: gene co-expression, protein interaction patterns.
- **Fraud / intrusion detection**: unusual combinations of actions.
- **Document/text mining**: term co-occurrence, topic discovery.

**Why not just use SQL `GROUP BY`?** Because the number of possible itemsets is exponential: with *d* items there are `2^d − 1` non-empty itemsets. d = 100 → about 1.27 × 10³⁰. Brute force is impossible, which is exactly why algorithms (Apriori, FP-Growth) and pruning principles exist.

---

## 2. The transaction data model

**Transaction database.** A set of transactions `D = {T₁, T₂, …, T_N}`, each `Tᵢ ⊆ I`, where `I = {i₁, i₂, …, i_d}` is the set of all items.

| TID | Items |
|---|---|
| T1 | Bread, Milk |
| T2 | Bread, Diapers, Beer, Eggs |
| T3 | Milk, Diapers, Beer, Coke |
| T4 | Bread, Milk, Diapers, Beer |
| T5 | Bread, Milk, Diapers, Coke |

**The vocabulary you must be able to define precisely:**

| Term | Definition |
|---|---|
| **Item** | a single element, e.g. `Milk` |
| **Itemset** | a set of one or more items, e.g. `{Milk, Bread}`; a **k-itemset** has k items |
| **Transaction** | one basket/record; a set of items |
| **Support count σ(X)** | the **number of transactions** containing itemset X |
| **Support s(X)** | the **fraction** of transactions containing X: `σ(X)/N` |
| **Frequent itemset** | an itemset with `support ≥ minsup` |
| **Association rule** | an implication `X → Y` where `X, Y` are disjoint itemsets (`X ∩ Y = ∅`) |
| **Confidence** | how often the rule is true: `c(X→Y) = σ(X∪Y)/σ(X)` |
| **Lift** | how much X improves the chance of Y: `lift = c(X→Y)/s(Y) = s(X∪Y)/(s(X)·s(Y))` |
| **Strong rule** | a rule with `support ≥ minsup` **and** `confidence ≥ minconf` |

---

## 3. Support

```
support(X) = (number of transactions containing X) / (total transactions) = σ(X)/N
```

*Using the table above (N = 5):*
- `σ({Bread}) = 4` → support = 0.8 (80 %)
- `σ({Milk, Diaper}) = 3` → support = 0.6 (60 %)
- `σ({Milk, Bread, Diaper}) = 2` → support = 0.4 (40 %)

**What support means in words:** *how common the combination is.* Low support → the pattern may be a coincidence (and would not be profitable to act on). High support → the pattern is frequent but may be too obvious to be interesting.

**Minimum support (minsup)** is set by the user — a business choice: 0.01 for 1 million transactions still means 10,000 baskets.

**Support is anti-monotonic** (downward closed): if `X ⊆ Y` then `support(Y) ≤ support(X)`. Adding an item can never increase the number of baskets containing the set. **This single property is what makes mining feasible** (see Topic 10).

---

## 4. Confidence

```
confidence(X → Y) = support(X ∪ Y) / support(X) = σ(X∪Y)/σ(X)
```

*Example:* with 5 transactions, `σ({Bread, Diaper}) = 3`, `σ({Bread}) = 4`:
```
Bread → Diaper:  confidence = 3/4 = 0.75 (75 %)
Diaper → Bread:  confidence = 3/3 = 1.00 (100 %)
```
**In words:** *of all the baskets containing Bread, 75 % also contained Diaper.* Confidence is **directional** — `X→Y` and `Y→X` are different rules with different confidences.

**Minimum confidence (minconf)** is the user's second threshold (commonly 0.5–0.7). Rules passing both thresholds are **strong association rules**.

**Limitation of confidence:** a high-confidence rule may be trivial. `{Milk} → {Bread}` with confidence 0.75 is unimpressive if **80 % of all baskets already contain Bread** — buying milk actually *slightly reduces* the chance of bread. Confidence alone cannot detect this; **lift** can. (This is the classic teaching point behind the "diapers → beer" story.)

---

## 5. Lift (and the other interestingness measures)

```
lift(X → Y) = confidence(X→Y) / support(Y) = s(X∪Y) / (s(X)·s(Y))
```

| Lift value | Interpretation |
|---|---|
| **lift = 1** | X and Y are **independent** — X tells you nothing about Y |
| **lift > 1** | **positive** association — X *increases* the chance of Y (useful for cross-selling) |
| **lift < 1** | **negative** association — X *decreases* the chance of Y (substitutes/competitors) |

*Worked:* `σ({Bread, Diaper}) = 3`, `σ(Bread) = 4`, `σ(Diaper) = 3`, N = 5.
`support(Bread ∪ Diaper) = 0.6`, `support(Bread) = 0.8`, `support(Diaper) = 0.6`.
`lift = 0.6 / (0.8 × 0.6) = 0.6/0.48 = 1.25` → buying bread raises the chance of buying diapers by 25 % — a genuine positive association.

**Other measures worth naming** (Topic 13 covers them in detail): **leverage** `s(X∪Y) − s(X)s(Y)`, **conviction** `(1 − s(Y))/(1 − c(X→Y))`, **χ²** (tests independence), **all-confidence**, **cosine**, **Kulczynski**, **Jaccard**.

**Support vs confidence vs lift in one line each:**
- **Support** = how often the rule applies (coverage, usefulness).
- **Confidence** = how reliable the rule is (accuracy, *given* the antecedent).
- **Lift** = how much better than chance the rule is (interestingness, correlation).

---

## 6. The mining task, stated formally

Given a transaction database `D`, a minimum support `minsup` and a minimum confidence `minconf`, find:
1. **All frequent itemsets** — every itemset X with `support(X) ≥ minsup`.
2. **All strong association rules** — every rule `X → Y` derived from a frequent itemset with `confidence ≥ minconf`.

**Two-phase structure (important — this is the architecture of every algorithm in this unit):**
```
Phase 1:  frequent itemset generation   (expensive — exponential search, pruned by support)
Phase 2:  rule generation               (cheap — from each frequent itemset, enumerate splits)
```
Because every rule `X→Y` derived from itemset `Z = X∪Y` automatically has `support(Z)`, support is computed **once** in phase 1 and reused in phase 2.

**Computational complexity of phase 1** (three factors to quote):
1. **Number of items (d)** — the search space is `2^d`.
2. **Number of transactions (N)** — each candidate needs a scan.
3. **Average transaction width** — wider baskets mean more/longer itemsets.

---

## 7. A complete small example (do this by hand until it is automatic)

| TID | Items |
|---|---|
| T1 | A, B, C |
| T2 | A, C |
| T3 | A, D |
| T4 | B, C |
| T5 | A, B, C |

`minsup = 40 %` of 5 = **2 transactions**; `minconf = 60 %`.

**Frequent itemsets:** `A(4), B(3), C(4), AB(2), AC(3), BC(3), ABC(2)` — `D(1)` is pruned.

**Rules from `{A, B, C}` (support 0.4):**

| Rule | Confidence | ≥ 0.6? |
|---|---|---|
| A → BC | 0.4/0.8 = 0.50 | ✗ |
| B → AC | 0.4/0.6 = 0.67 | ✓ |
| C → AB | 0.4/0.8 = 0.50 | ✗ |
| AB → C | 0.4/0.4 = 1.00 | ✓ |
| AC → B | 0.4/0.6 = 0.67 | ✓ |
| BC → A | 0.4/0.6 = 0.67 | ✓ |

So `{B → AC}`, `{AB → C}`, `{AC → B}`, `{BC → A}` are strong. Notice confidence is computed by dividing the *same* support of ABC by the support of the antecedent — no extra database scan. **Lift** for `AB → C`: `0.4/(0.4 × 0.8) = 1.25` → a real association.

---

## 8. Summary paragraph

Frequent pattern mining finds itemsets that co-occur often and turns them into rules `X → Y`. Three measures define everything: **support** = how often the itemset appears (coverage), **confidence** = how often Y appears when X does (reliability), **lift** = confidence divided by Y's base rate (interest beyond chance: 1 = independent, >1 positive, <1 negative). Mining has two phases — generate all frequent itemsets with support ≥ minsup, then derive rules with confidence ≥ minconf — and phase 1 is the expensive part because the itemset space is `2^d`. Its feasibility rests on the anti-monotonic property of support: **if an itemset is infrequent, every superset is infrequent too**, which is the Apriori principle.

---
**Next:** [Topic 10 — Apriori Algorithm: Working Principle](10-apriori-working-principle.md)
