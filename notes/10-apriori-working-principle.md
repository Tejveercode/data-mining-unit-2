# Topic 10 — Apriori Algorithm: Working Principle

> **LMS page:** *Chapter 2.3 — Apriori Algorithm: Working Principle* · **CO3**

---

## 1. Introduction

The **Apriori algorithm** (Agrawal & Srikant, 1994) is one of the earliest and most widely used algorithms for mining **frequent itemsets** and **association rules**. It is based on one idea: **any subset of a frequent itemset must also be frequent.** That property removes the vast majority of candidate itemsets before they are ever counted, which is what makes the search tractable.

Apriori is mainly used in **market basket analysis** — finding which items customers frequently buy together.

**Goal.** Efficiently identify **all itemsets whose support ≥ minimum support (minsup)**. Those frequent itemsets are then used to generate **strong association rules** with high confidence and lift.

**Why the name?** Because it uses *prior knowledge* of frequent itemset properties: it knows that if `{A, C}` is infrequent, then `{A, B, C}` cannot be frequent, so it never even tests it.

---

## 2. Key idea — level-wise, bottom-up search

Apriori performs a **bottom-up (level-wise) search**:

1. Start with **1-itemsets** (single items).
2. Keep the frequent ones.
3. **Join** them to form candidate **2-itemsets**; count support; keep the frequent ones.
4. **Join** frequent 2-itemsets → candidate 3-itemsets; prune; count; keep.
5. Continue, level by level, until **no further frequent itemsets can be generated**.

Every level requires **one full scan of the database** to count candidate supports. So Apriori makes `k_max + 1` scans for a maximum itemset size of `k_max` — the algorithm's main weakness (FP-Growth, Topic 12, fixes it).

**The two operations at each level:**
- **Join (candidate generation)** — combine frequent (k−1)-itemsets into k-itemsets.
- **Prune (candidate elimination)** — delete any candidate that contains an infrequent (k−1)-subset.

---

## 3. The Apriori property

> **If an itemset is frequent, then all of its subsets must also be frequent.**

Equivalently, and this is the form used for pruning:

> **If an itemset is infrequent, then all of its supersets must also be infrequent.**

**Why it is true (the one-line proof examiners want):** if a transaction contains the superset `ABC`, it necessarily contains every subset `AB`, `AC`, `BC`, `A`, `B`, `C`. So `σ(ABC) ≤ σ(AB)` for every subset — a superset can never be more frequent than its subset. Therefore if `σ(AB) < minsup`, then `σ(ABC) < minsup` too, and `ABC` can be discarded **without scanning the database**.

**The property is called _anti-monotonic_ (downward closed):** support is non-increasing as the itemset grows.

**Example.** If `AC` is infrequent, then `ABC`, `ACD`, `ABCE`, … — every itemset containing `AC` — is infrequent and is pruned immediately. In a 100-item dataset, this removes astronomically many candidates and is the entire reason Apriori works.

**Two corollaries worth quoting:**
- Every subset of a *frequent* itemset is frequent (used to keep candidates).
- Every superset of an *infrequent* itemset is infrequent (used to prune).

---

## 4. The Apriori algorithm — pseudocode

```
INPUT : transaction database D, minimum support minsup
OUTPUT: all frequent itemsets L

L₁ ← {frequent 1-itemsets}                      # scan D once, count every item
k  ← 2
while L_(k−1) ≠ ∅:

    # ---------- JOIN STEP ----------
    C_k ← join(L_(k−1), L_(k−1))                # combine pairs sharing k−2 items
                                                #   e.g. {A,B} ⋈ {A,C} → {A,B,C}

    # ---------- PRUNE STEP ----------
    for each candidate c ∈ C_k:
        if any (k−1)-subset of c is NOT in L_(k−1):
            delete c from C_k                   # Apriori property — no DB scan needed

    # ---------- COUNT STEP ----------
    for each transaction t ∈ D:                 # one full scan
        for each candidate c ∈ C_k:
            if c ⊆ t:  count[c] += 1

    L_k ← {c ∈ C_k : count[c] ≥ minsup}
    k   ← k + 1

return L₁ ∪ L₂ ∪ … ∪ L_(k−1)
```

### The join rule precisely

`L_(k−1)` itemsets are assumed sorted (items in lexicographic order). Two (k−1)-itemsets are joined **only if their first k−2 items are identical**; the k-itemset is formed from those shared items plus the two differing last items.

*Example:* `L₂ = {AB, AC, AD, BC, BD, CD}`.
`AB ⋈ AC` (share `A`) → `ABC`. `AB ⋈ AD` → `ABD`. `AC ⋈ AD` → `ACD`. `BC ⋈ BD` → `BCD`.
But `AB` and `CD` share nothing in the first k−2 = 0 positions... i.e. `AB` ends in `B`, `CD` in `D`, and their first item differs → not joined.

Then prune: `ABC` needs `AB, AC, BC` all frequent — if `BC ∉ L₂`, `ABC` is deleted without counting.

---

## 5. The steps of the working process (LMS six-step version — memorise this)

**Step 1.** Scan the database to find the **support of each individual item**. Those meeting minsup form the **frequent 1-itemset** `L₁`.

**Step 2.** Generate **candidate 2-itemsets** by combining the frequent 1-itemsets, then **scan the database** to compute their supports.

**Step 3.** **Prune** all candidate 2-itemsets that contain infrequent subsets (for 2-itemsets the subsets are just items, already filtered — pruning really bites from k = 3).

**Step 4.** Retain only the 2-itemsets meeting minsup — these are the **frequent 2-itemsets** `L₂`.

**Step 5.** **Repeat**: generate candidate 3-itemsets from `L₂`, prune using the Apriori property, count, keep.

**Step 6.** **Continue iterating** until no more frequent itemsets can be generated. Apriori terminates when `L_k` is empty (no candidates survive), or when no k-itemset can be formed.

---

## 6. A compact traced example (the shape of every Apriori answer)

Transactions: `T1={A,B,C}`, `T2={A,C}`, `T3={A,D}`, `T4={B,C}`, `T5={A,B,C}`; `minsup = 2` (40 % of 5).

**Level 1 — count items:**

| Item | Count | Frequent? |
|---|---|---|
| A | 4 | ✓ |
| B | 3 | ✓ |
| C | 4 | ✓ |
| D | 1 | ✗ (pruned) |

`L₁ = {A, B, C}` (`D` is dead — and with it every itemset containing D: `AD, BD, CD, ABD, ACD, BCD, ABCD` are never even generated).

**Level 2 — candidates from `L₁`:** `AB, AC, BC` (only 3 instead of all 6 pairs — pruning already at work).

| Candidate | Transactions | Count | Frequent? |
|---|---|---|---|
| AB | T1, T5 | 2 | ✓ |
| AC | T1, T2, T5 | 3 | ✓ |
| BC | T1, T4, T5 | 3 | ✓ |

`L₂ = {AB, AC, BC}`.

**Level 3 — join `L₂`:** `AB ⋈ AC → ABC` (share `A`); `AB ⋈ BC` → first items differ, no join; `AC ⋈ BC` → no join. Candidate set = `{ABC}`.
**Prune:** subsets `AB, AC, BC` are all in `L₂` → `ABC` survives.

| Candidate | Transactions | Count | Frequent? |
|---|---|---|---|
| ABC | T1, T5 | 2 | ✓ |

`L₃ = {ABC}`.

**Level 4:** no 4-itemset can be formed → **terminate**.

**Final frequent itemsets:** `A, B, C, AB, AC, BC, ABC` — 7 itemsets instead of the 15 non-empty subsets of {A,B,C,D}, and only 4 database scans.

---

## 7. Complexity and why Apriori can be slow

| Cost driver | Effect |
|---|---|
| **Number of scans** | one per level → `k_max + 1` scans; expensive on disk-based data |
| **Candidate generation** | `C_k` can explode (e.g. `10⁴` frequent 1-itemsets → ~5×10⁷ candidate pairs) |
| **Support counting** | each candidate tested against each transaction (subset matching) |
| **Long transactions** | wide baskets make subset checks costly |
| **Low minsup** | more frequent itemsets → more levels → more candidates (exponential blow-up) |

**Improvements to mention briefly:**
- **Hash-based counting** (hash buckets to cut candidate checks), **transaction reduction** (remove transactions with no frequent items), **partitioning** (partition the DB, mine locally, combine — two scans total), **sampling** (mine a sample, verify), **dynamic itemset counting** (DIC — interleave levels).
- **FP-Growth** (Topic 12) avoids candidate generation entirely by compressing the database into an FP-tree.

---

## 8. Merits and limitations (a balanced answer scores better)

**Merits**
- **Simple and easy to implement**; the logic is intuitive.
- **Provably complete** — it finds *all* frequent itemsets, no false negatives.
- **Massive pruning** via the anti-monotonic property.
- Works with any support definition and any itemset size; easy to parallelise level by level.

**Limitations**
- **Multiple database scans** (`k_max + 1`) — costly for large/streaming data.
- **Huge candidate sets** when there are many frequent items or minsup is low.
- **Slow on long patterns** and dense data (many items per transaction).
- **Memory heavy** — candidates must be held at each level.
- **Sensitive to the minsup threshold** — too high misses patterns, too low explodes.

---

## 9. Summary paragraph

Apriori finds all frequent itemsets by a **level-wise, bottom-up search**: count 1-itemsets, keep those ≥ minsup, join them into candidates, prune using the **Apriori property** (any superset of an infrequent itemset is infrequent, because `σ(superset) ≤ σ(subset)`), count the survivors with a database scan, and repeat until no candidates remain. Each level costs one scan, and the pruning is what makes an exponential problem tractable. Its strengths are simplicity and completeness; its weaknesses are repeated scans and explosive candidate generation — the gap that FP-Growth fills.

---
**Next:** [Topic 11 — Apriori Algorithm: Example Problems](11-apriori-example-problems.md)
