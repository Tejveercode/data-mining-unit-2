# Topic 13 — Mining Association Rules: Rule Generation & Interestingness Measures

> **LMS page:** *Chapter 2.3 — Mining Association Rules: Rule Generation, Interestingness Measures* · **CO3**
> *This page had not arrived when this was written, so the note is built from the course textbooks (Han Ch. 6.2–6.3, Tan Ch. 6.7) in the same style. It will be aligned with your page when it arrives.*

---

## 1. Where rule generation sits

Association mining has two phases:

```
Phase 1:  frequent itemset generation   ← Apriori (Topic 10) or FP-Growth (Topic 12)
Phase 2:  rule generation               ← this topic
```

**Why phase 2 is cheap:** every rule `X → Y` derived from a frequent itemset `Z = X ∪ Y` automatically inherits `support(Z)`. No new database scan is needed — only confidence arithmetic on supports already computed.

**The task.** From each frequent itemset `Z`, generate all rules `X → Z−X` (for every non-empty proper subset X) and keep those with `confidence ≥ minconf`. Such rules are called **strong** association rules; those satisfying both thresholds {support ≥ minsup, confidence ≥ minconf}.

> **Total possible rules from an itemset of size k:** `2^k − 2` (every non-empty proper subset as antecedent). For k = 10 that is 1,022 rules from one itemset — hence the need for the confidence pruning below.

---

## 2. Rule generation — the algorithm

**Confidence of a candidate rule** from frequent itemset `Z`, with antecedent `X ⊂ Z`, consequent `Y = Z − X`:
```
confidence(X → Y) = σ(Z) / σ(X)
```

**Key observation (the confidence monotonicity that enables pruning):** for a **fixed itemset Z**, `σ(Z)` is constant, so confidence depends only on `σ(X)`. As the antecedent `X` **grows**, `σ(X)` **shrinks**, so confidence **increases**. Equivalently, as the **consequent grows**, confidence falls.

**Therefore:** if a rule `X → Y` does **not** meet minconf, then **every rule with a smaller antecedent and larger consequent fails too** (e.g. if `{A,B} → {C,D}` fails, then `{A} → {B,C,D}` also fails). This lets us prune whole branches — the "Apriori of rules".

### 2.1 The algorithm (apriori-genrules)

```
for each frequent itemset Z:                     # sorted, k = |Z|
    H₁ = { single-item consequents h : h ∈ Z }   # 1-item consequents
    call GENRULES(Z, H₁)

GENRULES(Z, H_m):                                # H_m = set of m-item consequents
    if |Z| − m ≥ 1:
        for each h ∈ H_m:
            conf = σ(Z) / σ(Z − h)
            if conf ≥ minconf:  output rule (Z − h) → h
            else:               delete h from H_m       # prune
        H_(m+1) = APRIORI_GEN(H_m, minconf)      # join m-item consequents into (m+1)-item ones
        if H_(m+1) ≠ ∅: call GENRULES(Z, H_(m+1))
```

Two pruning ideas are used together:
1. **Confidence pruning** — a failing rule kills every rule whose consequent is a superset of it.
2. **Support pruning (built in)** — a rule's `Z` is frequent by construction, so support is never violated.

### 2.2 Full worked example (the one to know by heart)

Frequent itemset `Z = {A, B, C}`, `σ(Z) = 2`, `σ(A) = 4`, `σ(B) = 3`, `σ(C) = 4`, `σ(AB) = 2`, `σ(AC) = 3`, `σ(BC) = 3`, `N = 5`. **minconf = 60 %.**

**Level 1 — one-item consequents** (`conf = σ(ABC)/σ(antecedent)`):

| Rule | Confidence | ≥ 0.6? | Action |
|---|---|---|---|
| AB → C | 2/2 = **1.00** | ✓ | output |
| AC → B | 2/3 = **0.67** | ✓ | output |
| BC → A | 2/3 = **0.67** | ✓ | output |

All three pass → continue to level 2 (join consequents: `{C,B}`, `{C,A}`, `{B,A}`).

**Level 2 — two-item consequents:**

| Rule | Confidence | ≥ 0.6? | Action |
|---|---|---|---|
| A → BC | 2/4 = **0.50** | ✗ | **prune** — and with it any 3-item consequent |
| B → AC | 2/3 = **0.67** | ✓ | output |
| C → AB | 2/4 = **0.50** | ✗ | **prune** |

**Level 3** — consequents of size 3 would need antecedent size 0, which is not allowed → stop.

**Final strong rules:** `AB → C (1.00)`, `AC → B (0.67)`, `BC → A (0.67)`, `B → AC (0.67)`.

Notice: `A → BC` and `C → AB` failed because their antecedents are the *popular* items (A and C appear in 4 baskets, so conditioning on them is weak). **A confident rule needs a specific (low-support) antecedent and a common consequent** — a sentence worth writing in the exam.

---

## 3. Why support + confidence are not enough (the need for interestingness)

**The problem.** Support and confidence can both be satisfied by rules that are **trivially true, redundant, or misleading**. Four classic failures:

**(a) The trivial rule.** `{Milk} → {Bread}` with confidence 0.75 looks impressive — until you notice 80 % of all baskets contain bread. Buying milk actually *lowers* the chance of bread (lift 0.94). Confidence without a base-rate comparison is meaningless.

**(b) Independence.** If tea and coffee are bought independently at 50 % each, then `Tea → Coffee` has confidence 0.5 — a "rule" that says nothing. Lift = 1 exposes it.

**(c) Cross-support patterns (rare-item inflation).** Item `X` appears in 0.1 % of transactions, `Y` in 0.1 %, together in 0.09 % — **confidence near 90 %** with very low support. Such a rule usually describes a coincidence in a tiny sample, not a business pattern. *Remedy:* also require a minimum **support of the consequent** or use measures that correct for imbalance.

**(d) Simpson's paradox / confounding.** A rule can hold overall but reverse inside every subgroup (a drug looks helpful overall but harmful for both men and women). Aggregated association rules hide the confounder.

**The fix.** Add an **interestingness measure** (objective, data-driven, e.g. lift) or have a domain expert judge **subjective interestingness** (unexpectedness, actionability, novelty).

---

## 4. Objective interestingness measures

Let `X → Y`, with `P(X) = s(X)`, `P(Y) = s(Y)`, `P(XY) = s(X∪Y)`.

| Measure | Formula | Range | Meaning of the neutral point |
|---|---|---|---|
| **Support** | `P(XY)` | [0,1] | coverage / frequency of the rule |
| **Confidence** | `P(XY)/P(X)` | [0,1] | reliability given X |
| **Lift** | `P(XY)/(P(X)P(Y))` | [0,∞) | **1 = independent**, >1 positive, <1 negative |
| **Leverage** | `P(XY) − P(X)P(Y)` | [−0.25, 0.25] | **0 = independent**; the absolute "extra" co-occurrence |
| **Conviction** | `(1 − P(Y)) / (1 − confidence)` | [0,∞) | **1 = independent**; how strongly X implies Y (asymmetric) |
| **χ² (chi-square)** | `Σ (obs − exp)²/exp` over the 2×2 table | [0, N] | 0 = independent; needs significance testing |
| **All-confidence** | `min` over rules from itemset of confidence | [0,1] | how "tight" the whole itemset is |
| **Cosine** | `P(XY)/√(P(X)P(Y))` | [0,1] | 0 = independent |
| **Jaccard** | `P(XY)/(P(X)+P(Y)−P(XY))` | [0,1] | 0 = no overlap |
| **Kulczynski** | `½ [P(XY)/P(X) + P(XY)/P(Y)]` | [0,1] | average conditional probability, symmetric |

**Worked numbers** for `X → Y` with `P(X)=0.8, P(Y)=0.6, P(XY)=0.4`:
```
support    = 0.40
confidence = 0.40/0.80 = 0.500
lift       = 0.40/(0.80×0.60) = 0.833        → slightly negative association
leverage   = 0.40 − 0.48 = −0.080             → co-occur less than chance
conviction = (1−0.6)/(1−0.5) = 0.80           → < 1 confirms the negative direction
cosine     = 0.40/√(0.48) = 0.577
jaccard    = 0.40/(0.8+0.6−0.4) = 0.40
```
Every measure except support/confidence says this rule is **not worth acting on** — the lesson of the section.

### 4.1 Which measure should you use?

| Situation | Prefer |
|---|---|
| Retail cross-selling, balanced item frequencies | **lift** (simple, interpretable) |
| Need an absolute (not ratio) effect size | **leverage** |
| Direction matters and independence must be 1 | **conviction** |
| Very imbalanced supports (rare items) | **null-invariant measures**: cosine, Jaccard, Kulczynski, all-confidence |
| Statistical rigour, significance testing | **χ²** with a p-value (and note its weakness with small counts) |
| Explaining to a business audience | **support + confidence + lift**, in that order |

### 4.2 Null invariance (the modern, exam-extra point)

A measure is **null-invariant** if its value does **not** change when you add transactions containing **neither** X nor Y. Lift, χ², leverage and conviction are **not** null-invariant — adding irrelevant transactions changes them, and with very different supports (a 0.01 % item vs a 50 % item) they become misleading. **Cosine, Jaccard, Kulczynski and all-confidence are null-invariant**, so they are preferred for **cross-support** data. The practical compromise used in research (Tan et al.) is to **rank by Kulczynski and filter by support imbalance** (IR = imbalance ratio).

---

## 5. Subjective interestingness

Objective measures cannot know what the user already knows. **Subjective interestingness** asks whether a pattern is:
- **Unexpected** (not already known to the analyst),
- **Actionable** (leads to a decision or profit),
- **Novel** and **understandable**,
- **Corroborated** by other sources.

Hence systems add **templates / constraints**: `meta-rule guided mining` — e.g. only mine rules of the form `{product} → {product}` with `age ∈ [20,30]`, or rules involving a specific item of interest. Constraint pushing prunes the search enormously *and* keeps output relevant.

---

## 6. Redundancy and the output problem

Even with thresholds, rule sets contain **redundant rules**: if `A → BC` holds strongly, then `AB → C` and `AC → B` add little. Common compact representations:

| Concept | Definition | Why it helps |
|---|---|---|
| **Closed frequent itemset** | an itemset with **no proper superset of the same support** | the complete set of frequent itemsets with their supports can be derived from the closed ones — usually far fewer |
| **Maximal frequent itemset** | a frequent itemset with **no frequent proper superset** | most compact, but supports of subsets are lost (only bounds are known) |
| **Non-redundant / minimal rule set** | rules that cannot be derived from others | far smaller output for humans |

*Example:* if `{A,B}:3` and `{A,B,C}:3`, then `{A,B}` is **not closed** (its superset has equal support), while `{A,B,C}` is both **closed** and **maximal**.

---

## 7. Summary paragraph

Rule generation takes each frequent itemset `Z` and enumerates rules `X → Z−X`, keeping those with `confidence = σ(Z)/σ(X) ≥ minconf`; because confidence rises as the antecedent shrinks, a failing rule prunes every rule with a larger consequent, which keeps the output manageable. Support plus confidence alone, however, produce trivial, independent or rare-item-inflated rules, so **interestingness measures** are added: **lift** (`1` = independence, `>1` positive, `<1` negative), **leverage**, **conviction**, **χ²**, and the null-invariant **cosine, Jaccard, Kulczynski and all-confidence** for data with very different item frequencies. Output is then condensed using **closed**, **maximal** or **non-redundant** representations and constrained with meta-rules so that the final patterns are not merely statistically strong but genuinely **interesting and actionable**.

---
**End of notes.** Continue to the [revision cheat sheet](../exam/cheat-sheet.md) and the [question bank](../exam/question-bank.md).
