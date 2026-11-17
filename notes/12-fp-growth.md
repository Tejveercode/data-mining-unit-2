# Topic 12 — FP-Growth: Tree Construction & Pattern Extraction

> **LMS pages:** *Chapter 2.3 — FP-Growth Algorithm: Tree Construction* and *FP-Growth Algorithm: Pattern Extraction* · **CO3**
> *These pages had not arrived when this was written, so the note is built from the course textbooks (Han Ch. 6.6, Tan Ch. 6.4) in the same style and depth. It will be aligned with your pages when they arrive.*

---

## 1. Why FP-Growth exists

Apriori has two expensive habits:
1. **It scans the database once per level** — for long patterns that is many full passes over a huge file.
2. **It generates and counts candidate itemsets** — `C₂` alone can be millions of pairs (Topic 11, Problem 8).

**FP-Growth (Frequent Pattern Growth, Han et al. 2000)** removes both:
- **No candidate generation** — it never enumerates candidate itemsets.
- **Only two database scans** — after that it works entirely on an in-memory tree.

**Core idea:** compress the database into a compact tree structure (**FP-tree**) that preserves the itemset support information, then **grow** frequent patterns by recursively mining that tree, dividing the problem into smaller and smaller **conditional databases**.

---

## 2. The FP-tree structure

An **FP-tree (frequent-pattern tree)** is a prefix tree of transactions with three components:

1. **A root node** labelled `null`.
2. **Item-prefix subtrees** — each transaction is inserted as a path; nodes are labelled with an item name, and each node carries a **count** of how many transactions pass through it. **Shared prefixes are merged** and their counts incremented — this is the compression.
3. **A header table** — for every frequent item: its **support count** and a **node-link chain** threading all occurrences of that item through the tree (so a node can be found without scanning the tree).

**Key properties**
- Nodes higher in the tree are the more frequent items (the tree is built in **descending frequency order**, so shared prefixes are maximised and the tree stays small).
- A node's count ≥ the sum of its children's counts (a node is at least as frequent as any descendant path).
- The tree contains the **complete** support information of the database — no information is lost, so mining is exact, not approximate.

---

## 3. Building the FP-tree (construction algorithm)

**Input:** transaction database, `minsup`.

**Step 1 — Scan 1: find frequent 1-itemsets.** Count every item; discard items below minsup.

**Step 2 — Order items by descending support.** This ordering (a global order) is used for **every** transaction.

**Step 3 — Scan 2: build the tree.** For each transaction:
  - remove infrequent items;
  - sort the remaining items in the global order;
  - insert the resulting path into the tree; **increment counts** on existing nodes, create new ones as needed;
  - link each inserted node into its header-table chain.

**Step 4 — Done.** The FP-tree now represents the whole database.

### Worked construction (memorise this trace)

Transactions (`minsup = 2`): `T1 = {A,B,C}`, `T2 = {A,C}`, `T3 = {A,D}`, `T4 = {B,C}`, `T5 = {A,B,C}`.

**Scan 1 — item counts:**

| Item | Count | Frequent? |
|---|---|---|
| A | 4 | ✓ |
| B | 3 | ✓ |
| C | 4 | ✓ |
| D | 1 | ✗ (discarded — it can never be in a frequent itemset) |

**Step 2 — global order by descending frequency:** `A(4), C(4), B(3)`. (A and C tie at 4; break ties alphabetically — just state your rule.)

**Step 3 — reorder every transaction, dropping D:**

| TID | Original | Ordered path |
|---|---|---|
| T1 | A, B, C | **A, C, B** |
| T2 | A, C | **A, C** |
| T3 | A, D | **A** (D dropped) |
| T4 | B, C | **C, B** |
| T5 | A, B, C | **A, C, B** |

**Step 4 — insert one by one:**

```
Insert A,C,B (T1):        null → A:1 → C:1 → B:1
Insert A,C   (T2):        null → A:2 → C:2          (prefix shared, counts incremented)
Insert A     (T3):        null → A:3
Insert C,B   (T4):        null → A:3
                                └→ C:1 → B:1        (new branch from root)
Insert A,C,B (T5):        null → A:4 → C:3 → B:2    (counts incremented again)
```

**Final FP-tree**

```
          null
            │
          A:4
          ╱   ╲
     C:3       C:1
     │          │
    B:2        B:1
```

Rendered as paths: `A:4 → C:3 → B:2`, plus `C:1 → B:1` from the root.

**Header table**

| Item | Support | Node links |
|---|---|---|
| A | 4 | the single A:4 node |
| C | 4 | C:3 (under A), C:1 (under root) |
| B | 3 | B:2 (under A–C), B:1 (under root–C) |

**Notice the compression:** 5 transactions, 11 item occurrences → 6 nodes. In real data the compression is usually 10–100× because transactions share prefixes.

---

## 4. Mining the FP-tree (pattern extraction / growth)

The mining is **divide and conquer**: for each item (from the least frequent upward), collect the paths that reach it, build a **conditional pattern base**, then a **conditional FP-tree**, and mine that recursively. Every pattern found is prefixed by the item.

**The vocabulary (define it precisely):**
- **Prefix path**: the path from the root to a given node, *excluding* that node.
- **Conditional pattern base** of item X: all prefix paths of X, each paired with X's node count (paths are repeated for the count).
- **Conditional FP-tree** of X: the FP-tree built from X's conditional pattern base, keeping only items whose count in that base ≥ minsup.

### 4.1 Mining `B` (the least frequent item)

**Prefix paths of every B node:**
- `B:2` (under `A–C`) → prefix path `A, C` with count **2**
- `B:1` (under `C`) → prefix path `C` with count **1**

**Conditional pattern base of B:** `{A,C}:2`, `{C}:1`.

**Count items in that base:** `C = 2 + 1 = 3`, `A = 2`.
Both ≥ minsup (2) → **conditional FP-tree of B** contains the single path `C:3 → A:2`.

**Frequent patterns ending in B:**
```
{B}      : 3
{B, C}   : 3          (C:3 on the path)
{B, A}   : 2          (A:2 on the path)
{B, A, C}: 2          (whole path, min count 2)
```

### 4.2 Mining `C`

**Prefix paths of every C node:**
- `C:3` (under A) → prefix `A` with count 3
- `C:1` (under root) → empty prefix (contributes nothing)

**Conditional pattern base of C:** `{A}:3`. `A = 3 ≥ 2` → conditional FP-tree `A:3`.

**Frequent patterns ending in C:**
```
{C}    : 4
{A, C} : 3
```

### 4.3 Mining `A`

`A` has no prefix paths other than the root → conditional base empty → only `{A}: 4`.

### 4.4 Final result

```
{A}:4   {C}:4   {B}:3   {A,C}:3   {B,C}:3   {A,B}:2   {A,B,C}:2
```

**Identical to the Apriori answer from Topic 11** (A, B, C, AB, AC, BC, ABC with supports 4, 3, 4, 2, 3, 3, 2) — but produced **without ever generating a candidate itemset**, using only **2 database scans** and then pure in-memory tree operations. That is the whole point of the algorithm.

---

## 5. The FP-Growth algorithm (pseudocode)

```
FP-GROWTH(Tree, α):            # α = current prefix (suffix pattern being grown)
    if Tree is a single path P:
        for each combination β of nodes on P:
            output α ∪ β with support = min count on β
        return
    for each item a in the header table of Tree (bottom-up):
        β = α ∪ {a}
        output β with support = support(a)
        build the conditional pattern base of a
        build the conditional FP-tree Tree_β
        if Tree_β ≠ ∅:
            FP-GROWTH(Tree_β, β)
```

Two shortcuts worth naming:
- **Single-path optimisation:** if a conditional FP-tree is one path, all combinations of items on that path are frequent — output them directly without recursion.
- **Bottom-up order** (least frequent item first) keeps the conditional bases small.

---

## 6. FP-Growth vs Apriori — the comparison table

| Aspect | **Apriori** | **FP-Growth** |
|---|---|---|
| Candidate generation | **Yes** — join/prune at every level | **No** — grows patterns from the tree |
| Database scans | `k_max + 1` (one per level) | **2** |
| Main data structure | candidate sets + hash tree | **FP-tree** (compressed prefix tree) |
| Memory | candidates can explode | tree is compact but must **fit in memory** |
| Speed on dense / long data | slow (huge candidate sets) | **much faster** |
| Speed on sparse / short data | acceptable | also good, but tree overhead is relatively higher |
| Implementation complexity | simple | more complex |
| Sensitivity to minsup | high | lower, but very low minsup still yields a big tree |
| Exactness | exact | exact (no information lost in the tree) |
| Typical use | teaching, simple datasets | production mining, large datasets |

**One-line answer if asked "why is FP-Growth faster?"** *Because it scans the database only twice and then mines a compressed tree without ever generating or counting candidate itemsets; Apriori must re-scan the database for every level and test an exponentially growing candidate set.*

**Limitations of FP-Growth:** the tree must fit in main memory (a problem for very large/dense databases — solutions: partition the data, or use disk-based/tree-projection variants like FP-growth* and H-mine); building the tree is more complex to implement; and a very low minsup still produces a large tree.

---

## 7. Summary paragraph

FP-Growth compresses the transaction database into an **FP-tree** — a prefix tree where shared prefixes are merged and counts record how many transactions pass through each node, with a **header table** linking all occurrences of each item. Construction takes two scans: count items (drop infrequent ones), then insert each transaction as a frequency-ordered path, incrementing counts. Mining then proceeds by **divide and conquer**: for each item from least to most frequent, collect its **conditional pattern base** (its prefix paths), build the **conditional FP-tree**, and recurse — outputting every frequent pattern that ends in that item, with a single-path shortcut when the conditional tree is linear. The result is exactly the same frequent itemsets Apriori would find, but with **no candidate generation and only two database scans**, at the cost of a tree that must fit in memory and a more complex implementation.

---
**Next:** [Topic 13 — Mining Association Rules: Rule Generation & Interestingness Measures](13-rule-generation-interestingness.md)
