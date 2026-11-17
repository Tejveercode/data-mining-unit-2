# Topic 11 — Apriori Algorithm: Example Problems (fully solved)

> **LMS page:** *Chapter 2.3 — Apriori Algorithm: Example Problems* · **CO3**

This file contains the **five LMS problems solved step by step**, with the counting tables shown explicitly, followed by **three extra exam-style problems** with solutions. In an exam, marks come from the tables and the pruning reasoning — not from the final list.

---

## Problem 1 — Finding frequent itemsets using Apriori

**Dataset (5 transactions):**

| TID | Items |
|---|---|
| T1 | A, B, C |
| T2 | A, C |
| T3 | A, D |
| T4 | B, C |
| T5 | A, B, C |

**Minimum support = 40 %.** With 5 transactions, `minsup count = 0.40 × 5 = 2` transactions. (Always convert the percentage to a **count** first — it makes the table arithmetic trivial.)

### Step 1 — Support of 1-itemsets

| Item | Appears in | Count | Support | ≥ 2? |
|---|---|---|---|---|
| A | T1, T2, T3, T5 | **4** | 0.80 | ✓ |
| B | T1, T4, T5 | **3** | 0.60 | ✓ |
| C | T1, T2, T4, T5 | **4** | 0.80 | ✓ |
| D | T3 | **1** | 0.20 | ✗ |

**Frequent 1-itemsets:** `L₁ = {A, B, C}`. **D is removed** — and by the Apriori property, every itemset containing D (`AD, BD, CD, ABD, ACD, BCD, ABCD`) is infrequent and is never generated.

### Step 2 — Candidate 2-itemsets from `L₁`

Only three pairs are possible: `AB, AC, BC`.

| Candidate | Appears in | Count | Support | ≥ 2? |
|---|---|---|---|---|
| AB | T1, T5 | 2 | 0.40 | ✓ |
| AC | T1, T2, T5 | 3 | 0.60 | ✓ |
| BC | T1, T4, T5 | 3 | 0.60 | ✓ |

All three meet the threshold → `L₂ = {AB, AC, BC}`.

### Step 3 — Candidate 3-itemset

Join: `AB ⋈ AC → ABC` (they share `A`). Prune check: subsets of `ABC` are `AB, AC, BC` — **all are in `L₂`**, so `ABC` is a valid candidate.

| Candidate | Appears in | Count | Support | ≥ 2? |
|---|---|---|---|---|
| ABC | T1, T5 | 2 | 0.40 | ✓ |

### Result
```
Frequent itemsets = {A}, {B}, {C}, {AB}, {AC}, {BC}, {ABC}
```
Total **7** itemsets. Note the saving: the brute-force space was `2⁴ − 1 = 15`; Apriori needed only 4 + 3 + 1 = 8 support counts.

---

## Problem 2 — Support, confidence and lift from the same data

Using the results above, generate and evaluate rules from the frequent itemset **`ABC`**.

**Total transactions N = 5.** `σ(ABC) = 2`, so `support(ABC) = 2/5 = 0.4 (40 %)`.

**All rules from `ABC`** (`confidence = σ(ABC)/σ(antecedent)`):

| Rule | σ(antecedent) | Confidence | Lift |
|---|---|---|---|
| A → BC | σ(A) = 4 | 2/4 = **0.50** | 0.4 / (0.8 × 0.6) = **0.833** |
| B → AC | σ(B) = 3 | 2/3 = **0.667** | 0.4 / (0.6 × 0.6) = **1.111** |
| C → AB | σ(C) = 4 | 2/4 = **0.50** | 0.4 / (0.8 × 0.4) = **1.25** |
| AB → C | σ(AB) = 2 | 2/2 = **1.00** | 0.4 / (0.4 × 0.8) = **1.25** |
| AC → B | σ(AC) = 3 | 2/3 = **0.667** | 0.4 / (0.6 × 0.6) = **1.111** |
| BC → A | σ(BC) = 3 | 2/3 = **0.667** | 0.4 / (0.6 × 0.8) = **0.833** |

**The LMS rule `A → BC`, worked exactly as the page does it:**
- `support(A→BC) = support(ABC) = 0.4`
- `confidence(A→BC) = support(ABC)/support(A) = 0.4/0.8 = 0.5 (50 %)`
- `lift(A→BC) = support(ABC) / (support(A) × support(BC)) = 0.4 / (0.8 × 0.6) = 0.4/0.48 = 0.833`

**Interpretation (state this sentence in the exam):** lift < 1 means A does **not** increase the likelihood of buying B and C together — the items are slightly **negatively** associated, so this is not a useful cross-selling rule despite the itemsets being frequent.

If `minconf = 60 %`, the strong rules are `B→AC`, `AB→C`, `AC→B`, `BC→A`.

---

## Problem 3 — Apriori with a higher support threshold

**Dataset:**

| TID | Items |
|---|---|
| T1 | Milk, Bread |
| T2 | Bread, Butter |
| T3 | Milk, Bread, Butter |
| T4 | Bread |
| T5 | Milk, Butter |

**Minimum support = 3 occurrences** (60 % of 5).

### Step 1 — 1-itemsets

| Item | Appears in | Count | ≥ 3? |
|---|---|---|---|
| Milk | T1, T3, T5 | **3** | ✓ |
| Bread | T1, T2, T3, T4 | **4** | ✓ |
| Butter | T2, T3, T5 | **3** | ✓ |

`L₁ = {Milk, Bread, Butter}` — all items survive.

### Step 2 — 2-itemsets

| Candidate | Appears in | Count | ≥ 3? |
|---|---|---|---|
| Milk + Bread | T1, T3 | 2 | ✗ |
| Milk + Butter | T3, T5 | 2 | ✗ |
| Bread + Butter | T2, T3 | 2 | ✗ |

**None** reaches 3. Therefore `L₂ = ∅`, and since no larger itemset can exist without a frequent 2-subset (Apriori property), the algorithm **terminates at level 2**.

### Result
```
Frequent itemsets = {Milk}, {Bread}, {Butter}   (1-itemsets only)
```

**Teaching point:** with `minsup = 2` instead of 3, all three pairs would be frequent and `{Milk, Bread, Butter}` (count 1) would still fail. A high support threshold yields only trivial, obvious rules — this is the **support trade-off**: too high → nothing interesting, too low → combinatorial explosion and spurious rules.

---

## Problem 4 — Pruning using the Apriori property

**Dataset:**

| TID | Items |
|---|---|
| T1 | A, B |
| T2 | A, C |
| T3 | B, C |
| T4 | A, B, C |

**Minimum support = 2.**

**1-itemsets:** A in T1,T2,T4 = 3; B in T1,T3,T4 = 3; C in T2,T3,T4 = 3 → `L₁ = {A, B, C}`.

**2-itemsets:** AB in T1,T4 = 2; AC in T2,T4 = 2; BC in T3,T4 = 2 → `L₂ = {AB, AC, BC}` (all frequent).

**3-itemset candidate `ABC`:** before counting, apply the Apriori property — all 2-subsets `AB, AC, BC` are in `L₂`, so `ABC` **is a valid candidate**.

| Candidate | Appears in | Count | ≥ 2? |
|---|---|---|---|
| ABC | T4 only | **1** | ✗ → **pruned** |

### Result
```
Frequent itemsets = {A}, {B}, {C}, {AB}, {AC}, {BC}    (ABC is pruned: support 1 < 2)
```

**The point of this problem:** `ABC` was generated legitimately (its subsets are frequent) — the *pruning* happened on **support**, not on the Apriori property. The Apriori property prunes candidates *before* counting; support pruning happens *after*. Be precise about which is which.

---

## Problem 5 — Using Apriori to build a recommendation rule

**Dataset:**

| TID | Items |
|---|---|
| T1 | Tea, Biscuit |
| T2 | Tea, Sugar |
| T3 | Tea, Biscuit, Sugar |
| T4 | Biscuit |
| T5 | Tea, Biscuit |

**Minimum support = 2.**

### Step 1 — 1-itemsets
Tea: T1,T2,T3,T5 = **4**; Biscuit: T1,T3,T4,T5 = **4**; Sugar: T2,T3 = **2** → `L₁ = {Tea, Biscuit, Sugar}`.

### Step 2 — 2-itemsets

| Candidate | Appears in | Count | ≥ 2? |
|---|---|---|---|
| Tea + Biscuit | T1, T3, T5 | **3** | ✓ |
| Tea + Sugar | T2, T3 | **2** | ✓ |
| Biscuit + Sugar | T3 | **1** | ✗ (removed) |

`L₂ = {Tea Biscuit, Tea Sugar}`. Since `Biscuit Sugar` is infrequent, the 3-itemset `{Tea, Biscuit, Sugar}` is **pruned without counting** (its subset `Biscuit Sugar` is infrequent) — a clean demonstration of the Apriori property.

### Step 3 — Rule from `{Tea, Biscuit}`

```
Rule:  Tea → Biscuit
support    = 3/5 = 0.60   (60 % of all baskets contain both)
confidence = support(Tea ∪ Biscuit) / support(Tea) = 0.6 / 0.8 = 0.75  (75 %)
lift       = 0.6 / (0.8 × 0.8) = 0.9375
```
**Interpretation:** *75 % of customers who buy Tea also buy Biscuit* — a useful cross-selling rule by confidence, though lift slightly below 1 says biscuits are already so popular that tea does not add much. (The reverse rule `Biscuit → Tea` has confidence 3/4 = 0.75 as well, because the supports coincide.)

---

## Extra Problem 6 — Apriori on a 6-transaction dataset with a 30 % threshold

| TID | Items |
|---|---|
| T1 | I1, I2, I5 |
| T2 | I2, I4 |
| T3 | I2, I3 |
| T4 | I1, I2, I4 |
| T5 | I1, I3 |
| T6 | I2, I3 |

`minsup = 30 %` of 6 = **1.8 → 2 transactions** (always round **up**).

**Level 1:** I1: T1,T4,T5 = 3 ✓ · I2: T1,T2,T3,T4,T6 = 5 ✓ · I3: T3,T5,T6 = 3 ✓ · I4: T2,T4 = 2 ✓ · I5: T1 = 1 ✗.
`L₁ = {I1, I2, I3, I4}` — **I5 pruned**, so `I1I2I5`, `I1I5`, `I2I5`… never appear.

**Level 2** (from the 4 surviving items, 6 pairs): I1I2 = T1,T4 = 2 ✓ · I1I3 = T5 = 1 ✗ · I1I4 = T4 = 1 ✗ · I2I3 = T3,T6 = 2 ✓ · I2I4 = T2,T4 = 2 ✓ · I3I4 = 0 ✗.
`L₂ = {I1I2, I2I3, I2I4}`.

**Level 3:** join `I1I2 ⋈ I2I3` → `I1I2I3`; prune: subset `I1I3` ∉ `L₂` → **pruned before counting**. Join `I1I2 ⋈ I2I4` → `I1I2I4`; subset `I1I4` ∉ `L₂` → **pruned**.
`L₃ = ∅` → terminate.

**Answer:** `{I1}, {I2}, {I3}, {I4}, {I1I2}, {I2I3}, {I2I4}`. Note that the two level-3 candidates were killed by pruning, **not** by a database scan — that is exactly the efficiency Apriori buys.

---

## Extra Problem 7 — Compute support, confidence and lift for a given rule

Transactions: 10 baskets; `{Milk, Bread}` appears in 4; `Milk` in 6; `Bread` in 8.

```
support(Milk ∪ Bread) = 4/10 = 0.40
confidence(Milk → Bread) = 0.40 / 0.60 = 0.667   (66.7 %)
lift(Milk → Bread) = 0.40 / (0.60 × 0.80) = 0.40/0.48 = 0.833
```
and in the other direction:
```
confidence(Bread → Milk) = 0.40 / 0.80 = 0.50
lift = 0.833   (lift is symmetric — confidence is not)
```
**Conclusion:** both lifts are identical (0.833 < 1) → milk and bread are slightly **negatively** associated; the rules are "strong" by confidence but **not interesting** by lift. This is the single most common exam trap in association mining.

---

## Extra Problem 8 — How many candidates does Apriori generate?

`L₁` has 100 frequent items. How many candidate 2-itemsets does the join produce, and why is pruning powerless here?

`C₂ = C(100,2) = 100×99/2 = **4,950**` candidates, requiring one pass to count. The Apriori property **cannot prune any of them**, because every 2-itemset's only proper subsets are 1-itemsets, all of which are frequent (that is why they are in `L₁`). This is why Apriori is slow on data with many frequent items, and why FP-Growth exists.

---

## Answer-writing checklist for any Apriori problem

1. **Convert minsup % to a count**: `count = ceil(minsup × N)`. State it.
2. **Draw a table per level**: candidate | transactions containing it | count | frequent?
3. **Show the pruning step explicitly** — write "*p ⊆ c and p ∉ L₂ → c pruned*" for at least one candidate.
4. **List `L₁, L₂, L₃ …` separately** and state where the algorithm **terminates** (and why).
5. For rules: **support = σ(X∪Y)/N**, **confidence = σ(X∪Y)/σ(X)**, **lift = s(X∪Y)/(s(X)·s(Y))**.
6. **Interpret** every rule in words, and say whether lift > 1 makes it worth acting on.

---
**Next:** [Topic 12 — FP-Growth Algorithm](12-fp-growth.md)
