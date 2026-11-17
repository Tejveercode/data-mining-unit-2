# Topic 12 — FP-Growth: Tree Construction & Pattern Extraction

> **LMS pages:** *Chapter 2.3 — FP-Growth Algorithm: Tree Construction* and *FP-Growth Algorithm: Pattern Extraction* · **CO3**
> Both pages are covered in full, using **your page's dataset** (T1: A,B · T2: B,C,D · T3: A,C,D · T4: A,B,C · T5: B,C · minsup = 2). All counts below have been verified by running the algorithm.

---

# PART A — FP-TREE CONSTRUCTION

## A1. Introduction to FP-Growth

**FP-Growth (Frequent Pattern Growth)** is an advanced algorithm for mining frequent itemsets **without generating candidate itemsets**. It overcomes the major limitations of Apriori by **compressing the database into a compact data structure called an FP-Tree**. The FP-Tree allows mining of frequent patterns through **recursive exploration of conditional trees**.

It is widely used because it is **faster and more memory-efficient than Apriori**, especially for **large or dense** datasets.

## A2. Motivation: the two phases

**Why Apriori is slow:** it requires **multiple database scans** and generates a **large number of candidate itemsets**, which slows the process down. FP-Growth avoids both by using **only two database scans** and compressing the data into a tree.

**The algorithm works in two phases:**
```
Phase 1: Construct the FP-Tree
Phase 2: Mine the FP-Tree using conditional pattern bases and conditional FP-Trees
```
Part A of this note is Phase 1; Part B is Phase 2.

## A3. What is an FP-Tree

An **FP-Tree (Frequent Pattern Tree)** is a **compressed representation of the transactional database**. It stores the items of each transaction as a **path**, **sharing common prefixes** wherever possible. **Only frequent items appear** in the tree, and the **counts** on nodes reflect how many times each path occurs in the dataset.

**An FP-Tree consists of four parts:**
1. A **root node labelled `null`**.
2. **Item nodes** storing the item name and its frequency.
3. **Links** connecting identical items across different branches (node links).
4. A **header table** containing each frequent item and a link to its **first occurrence** in the tree.

## A4. Steps in FP-Tree construction (two database scans)

**Step 1 — First database scan: find frequent items.**
Scan the database to determine the **support count of each item**. **Remove items** that do not meet the minimum support threshold. **Sort the remaining frequent items in descending order of support.**
*Why:* this ensures the most frequent items appear first, **maximising compression** (shared prefixes).

**Step 2 — Initialise the FP-Tree.**
Create a **root node labelled `null`**. Prepare the **header table**, each entry containing:
- the item name,
- the frequency count,
- a **link to the first node** of this item in the tree.

**Step 3 — Second database scan: insert the transactions.**
For each transaction:
1. **remove infrequent items**,
2. **sort** the remaining items in descending global frequency,
3. **insert** the ordered items as a **path** in the tree:
   - if the **prefix already exists**, **increase the count** of the existing nodes;
   - if not, **create new nodes** along the path;
4. **update the header-table links** to connect nodes of the same item across branches.

## A5. Worked construction on your page's dataset

**Transactions, minimum support = 2:**

| TID | Items |
|---|---|
| T1 | A, B |
| T2 | B, C, D |
| T3 | A, C, D |
| T4 | A, B, C |
| T5 | B, C |

### Step 1 — Count item frequency (first scan)

| Item | Appears in | Count | ≥ 2? |
|---|---|---|---|
| A | T1, T3, T4 | **3** | ✓ |
| B | T1, T2, T4, T5 | **4** | ✓ |
| C | T2, T3, T4, T5 | **4** | ✓ |
| D | T2, T3 | **2** | ✓ |

**All items are frequent** (D only just — a nice reminder that `= minsup` counts as frequent).

**Descending support order:** `B(4), C(4), A(3), D(2)`. (B and C tie at 4; your page puts **B first** — always state the tie-break you use, because it fixes the tree shape.)

### Step 2 — Reorder every transaction by that global order

| TID | Original | Reordered |
|---|---|---|
| T1 | A, B | **B, A** |
| T2 | B, C, D | **B, C, D** |
| T3 | A, C, D | **C, A, D** |
| T4 | A, B, C | **B, C, A** |
| T5 | B, C | **B, C** |

Note T3: it does **not** start with B, so it opens a **second branch from the root**. This is the detail students get wrong.

### Step 3 — Insert one by one (second scan)

```
Insert B,A    (T1):  null → B:1 → A:1
Insert B,C,D  (T2):  null → B:2 → C:1 → D:1        (B shared, count → 2)
Insert C,A,D  (T3):  null → C:1 → A:1 → D:1        (new branch: C is not a child of the root yet)
Insert B,C,A  (T4):  null → B:3 → C:2 → A:…        (B, C shared; new A node under B-C)
                     → A:  B-C chain gains a second A node, count 1
Insert B,C    (T5):  null → B:4 → C:3              (all shared, counts incremented)
```

**Final FP-Tree**

```
                null
              ╱      ╲
           B:4        C:1
          ╱   ╲         ╲
       A:1    C:3        A:1
             ╱   ╲         ╲
          D:1    A:1        D:1
```

Equivalently, as root-to-leaf paths:
```
B:4 → A:1
B:4 → C:3 → D:1
B:4 → C:3 → A:1
C:1 → A:1 → D:1
```

**Header table**

| Item | Support | Node links (chain) |
|---|---|---|
| **B** | 4 | B:4 |
| **C** | 4 | C:3 (under B) → C:1 (under root) |
| **A** | 3 | A:1 (under B) → A:1 (under B–C) → A:1 (under root-C) |
| **D** | 2 | D:1 (under B–C) → D:1 (under root-C–A) |

**The compression, quantified:** 5 transactions contain **12 item occurrences** (2+3+3+3+2), yet the tree has only **10 nodes** — and the shared prefixes `B`, `B–C` are stored **once each** while representing 4 and 3 transactions respectively. That is the entire point of the structure.

## A6. Header table and node links (why they exist)

The header table keeps track of the **first occurrence** of each item; each entry has a **pointer to the first node** of that item in the tree, and additional nodes with the same item are **linked through a node-link chain**.

**Example for item C:** the header entry for C points to the **first C node** (C:3 under B); that node links to the **next C node** (C:1 under the root), and so on.

**Why it matters:** this linking is what makes **conditional FP-Tree construction fast** — it lets the algorithm jump directly to *all* occurrences of an item without scanning the tree.

## A7. Advantages of FP-Tree construction (six, from your page)

- Requires **only two database scans**.
- **Eliminates the need to generate candidate itemsets**.
- **Compresses** the database into a smaller structure.
- **Reduces repeated scanning** of transactions.
- **Efficient for large and dense** transactional datasets.
- **Shared prefixes reduce redundancy** and improve storage utilisation.

## A8. Limitations of FP-Tree construction

- The FP-Tree **may still become large when items rarely overlap** across transactions (sparse data → little prefix sharing → little compression).
- It is **difficult to construct for extremely high-dimensional** data.
- Mining **multiple conditional FP-Trees requires recursive logic**.
- **Implementation is more complex** than Apriori.

## A9. Key insight of FP-Tree construction

Represent the dataset in a **compact form by grouping frequent items into shared paths**. This avoids repeated scanning and reduces the computations needed to find frequent patterns. **The FP-Tree is the foundation for fast mining of association rules.**

---

# PART B — PATTERN EXTRACTION

## B1. Introduction

FP-Growth mines frequent itemsets **without generating candidates**. After the FP-Tree is built, the next major step is **extracting frequent patterns** from it. This is done by building **conditional pattern bases** and **conditional FP-Trees** for each item.

**Pattern extraction is recursive and explores the FP-Tree from the bottom of the header table upward** (least frequent item first — because its conditional base is the smallest).

## B2. What is a conditional pattern base

A **conditional pattern base** is a **sub-database consisting of prefix paths that co-occur with a particular item**. It represents all transactions that support that item.

For a given item X, the conditional pattern base contains **the paths from the FP-Tree that lead to X, along with their frequency counts**.

*Example:* if item C appears under different branches, the prefix paths leading to those occurrences form the conditional pattern base for C.

**Conditional pattern bases are used to create conditional FP-Trees.**

## B3. Conditional FP-Tree

A **conditional FP-Tree is a smaller FP-Tree constructed from the conditional pattern base of an item**. It contains **only the items that co-occur with the given item and meet the minimum support threshold**.

- If the conditional FP-Tree contains **only one path**, **all combinations** of items on that path form frequent itemsets.
- If it contains **multiple paths**, **recursive mining** is performed on it.

Building conditional FP-Trees **reduces the complexity of mining** and lets FP-Growth find frequent itemsets efficiently.

## B4. The seven steps of pattern extraction (your page's procedure)

**Step 1.** Select an item from the **bottom** of the header table. This item becomes the **suffix** of the potential frequent patterns.
**Step 2.** Retrieve the **conditional pattern base** for this item by following its **node links** in the FP-Tree.
**Step 3.** **Construct the conditional FP-Tree** from that base. **Remove infrequent items** from the conditional FP-Tree.
**Step 4.** If the conditional FP-Tree is **empty**, stop — no more patterns can be generated for this item.
**Step 5.** If the conditional tree has a **single path**, generate **all combinations** of items on that path, combined with the suffix item. These are frequent patterns.
**Step 6.** If the conditional FP-Tree has **multiple branches**, **recursively repeat** FP-Growth to generate patterns.
**Step 7.** **Move to the next item** in the header table and repeat.

## B5. Worked extraction on the tree from Part A (verified counts)

Header order bottom-up: **D (2) → A (3) → C (4) → B (4)**.

### Mining D (least frequent)

**Prefix paths leading to D** (follow the D node links on your page's tree):

| D node | Prefix path | Transaction |
|---|---|---|
| D:1 (under B–C) | **B, C** | T2 |
| D:1 (under C–A) | **C, A** | T3 |

**Conditional pattern base of D:** `{B,C}:1`, `{C,A}:1`.

**Counts in that base:** **C = 2**, B = 1, A = 1. With `minsup = 2`, **only C survives**.

**Conditional FP-Tree of D:** a **single path** `C:2` → by Step 5, all combinations with D are frequent:
```
{D, C}: 2      ← the only frequent pattern ending in D
```
The other combinations permitted by the shape of the tree — `{D,B}`, `{D,A}`, `{D,B,C}`, `{D,A,C}`, `{D,A,B}`, `{D,A,B,C}` — each have **support 1**, so they are **not frequent**.

> **Exam point worth stating explicitly:** a single-path conditional tree tells you **which combinations exist**, but you must still report the **support** (the minimum count on the path) and check it against minsup. Your page's illustrative list shows the *shape* of the output; the counts are what decide which of those patterns actually qualify.

### Mining A

**Prefix paths of every A node:** `{B}:1` (T1), `{B,C}:1` (T4), `{C}:1` (T3).
**Counts:** **B = 2, C = 2** → both survive.
**Patterns ending in A:** `{A,B}: 2`, `{A,C}: 2` (`{A,B,C}` has support 1 → not frequent).

### Mining C

**Prefix paths:** `{B}:3` (the C:3 node), empty prefix (the C:1 node under the root contributes nothing).
**Conditional FP-Tree:** single path `B:3` → **`{B,C}: 3`**.

### Mining B

B has only the root as its prefix → conditional base empty → **`{B}: 4`** (no larger pattern ends in B).

### Final result

```
{A}:3   {B}:4   {C}:4   {D}:2   {A,B}:2   {A,C}:2   {B,C}:3   {C,D}:2
```

**Verification by brute force** (support counts straight from the data):

| Itemset | Transactions | Count | Frequent? |
|---|---|---|---|
| AB | T1, T4 | 2 | ✓ |
| AC | T3, T4 | 2 | ✓ |
| AD | T3 | 1 | ✗ |
| BC | T2, T4, T5 | 3 | ✓ |
| BD | T2 | 1 | ✗ |
| CD | T2, T3 | 2 | ✓ |
| ABC | T4 | 1 | ✗ |
| BCD | T2 | 1 | ✗ |
| ACD | T3 | 1 | ✗ |

**Exactly the eight itemsets FP-Growth produced** — and the same eight Apriori would produce. This is the answer to reproduce if you are asked to run FP-Growth on this dataset.

## B6. Single-path conditional FP-Trees (the shortcut)

If the conditional FP-Tree contains **only one branch**, extraction is simple — **no recursion is needed**.

**Example branch:** `X → Y → Z`. With suffix item **W**, the frequent combinations are:
```
W X    W Y    W Z    W X Y    W X Z    W Y Z    W X Y Z
```
i.e. **every subset of the path's items, joined with the suffix** — `2³ − 1 = 7` patterns from a 3-item path. In general a path of length *k* yields `2^k − 1` patterns (before the minsup check on counts).

## B7. Multi-path conditional FP-Trees

If the conditional FP-Tree has **multiple branches**, **recursive mining is necessary**: each branch contributes different prefix paths, so FP-Growth must **explore each branch separately**, creating **smaller and smaller conditional FP-Trees** until the patterns are fully extracted.

This recursive structure is exactly what allows FP-Growth to **avoid generating the large candidate sets that Apriori needs**.

## B8. Advantages of FP-Growth pattern extraction

- **Avoids exponential candidate generation.**
- Uses a **compressed structure**, reducing database scans.
- Handles **dense datasets** efficiently.
- **Recursion allows clean separation** of conditional patterns.
- **Works faster than Apriori** for most practical datasets.

## B9. Limitations of FP-Growth pattern extraction

- **Conditional trees may still become large** for sparse datasets.
- **Recursion adds implementation complexity.**
- The FP-Tree **needs enough memory** to store all branches and node links.
- **Interpretation of conditional trees may be difficult for beginners.**

---

## B10. FP-Growth vs Apriori — the comparison to write in the exam

| Aspect | **Apriori** | **FP-Growth** |
|---|---|---|
| Candidate generation | yes — join and prune at every level | **none** |
| Database scans | `k_max + 1` (one per level) | **2** |
| Core structure | candidate sets + hash tree | **FP-Tree** + header table |
| Memory | candidates can explode | compact tree, but must **fit in RAM** |
| Speed on dense/long data | slow | **much faster** |
| Implementation | simple | more complex (recursive) |
| Result | all frequent itemsets | **the same** all frequent itemsets |

**One-line answer to "why is FP-Growth faster?"** *Because it reads the database only twice and then mines a compressed tree without ever generating or counting candidate itemsets, whereas Apriori re-scans the database at every level and tests an exponentially growing candidate set.*

---

## B11. Summary paragraph

FP-Growth has two phases. **Construction:** scan once to count items and drop the infrequent ones, order the survivors by descending support, then scan again to insert each transaction as a frequency-ordered path into a tree of shared prefixes whose nodes carry counts, with a header table chaining all occurrences of each item. **Extraction:** work from the bottom of the header table upward; for each item collect its **conditional pattern base** (the prefix paths reaching it, with counts), build the **conditional FP-Tree** keeping only items that still meet minsup, then either enumerate all combinations if the tree is a single path or recurse if it has several branches. On your page's own dataset (minsup = 2) this yields `{A}:3, {B}:4, {C}:4, {D}:2, {A,B}:2, {A,C}:2, {B,C}:3, {C,D}:2` — identical to Apriori's result, obtained with two scans and zero candidate sets.

---
**Next:** [Topic 13 — Mining Association Rules: Rule Generation & Interestingness Measures](13-rule-generation-interestingness.md)
