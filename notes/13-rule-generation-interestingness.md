# Topic 13 — Mining Association Rules: Rule Generation & Interestingness Measures

> **LMS page:** *Chapter 2.3 — Mining Association Rules: Rule Generation, Interestingness Measures* · **CO3**
> Written to your page's structure and using its examples (`{A,B,C}` rule list and the Bread/Milk/Butter support table), with the standard theory added where your page points to it.

---

# PART A — RULE GENERATION

## A1. Introduction to association rule mining

**Association rule mining is the process of discovering meaningful relationships among items in transactional data.**

Once **frequent itemsets** are discovered using **Apriori or FP-Growth**, the next step is to **generate association rules from those itemsets**. The rules explain **how items or events are related** and are widely used in **retail, recommendation systems, fraud detection and marketing**.

**Association rules are expressed as `X → Y`**, meaning: *when X occurs, Y is likely to occur.* (Formally `X ∩ Y = ∅`, with `X` the **antecedent** and `Y` the **consequent**.)

## A2. What rule generation is

**Rule generation is the process of creating valid association rules from frequent itemsets that satisfy minimum confidence and other interestingness measures.**

- A frequent itemset can generate **many** possible rules.
- **Only rules that meet the required thresholds are selected.**

**Your page's example:** from the frequent itemset **`{A, B, C}`** the possible rules are:

| # | Rule |
|---|---|
| 1 | `A → B C` |
| 2 | `B → A C` |
| 3 | `C → A B` |
| 4 | `A B → C` |
| 5 | `A C → B` |
| 6 | `B C → A` |

That is `2³ − 2 = 6` rules — in general a k-itemset yields **`2^k − 2`** rules (every non-empty proper subset as antecedent), which is why pruning is essential at k = 10 (1,022 rules) and beyond.

**Each rule must be evaluated using support, confidence and other metrics.**

## A3. The six steps of rule generation (your page — memorise the sequence)

**Step 1.** Identify all **frequent itemsets** that satisfy minimum support.
**Step 2.** For each frequent itemset, list **all possible non-empty subsets**.
**Step 3.** For each subset X, generate a rule of the form **`X → (itemset − X)`**.
**Step 4.** Calculate the **confidence** of each rule and compare it with **minimum confidence**.
**Step 5.** **Discard** rules that fail to meet the confidence threshold.
**Step 6.** Evaluate the remaining rules using **additional interestingness measures** to ensure they are meaningful.

*This systematic approach ensures only strong and relevant rules are generated.*

### A3.1 The confidence formula and the pruning trick (the exam-grade detail)

```
confidence(X → Y) = support(X ∪ Y) / support(X) = σ(X∪Y)/σ(X)
```
**Support is free** — every rule from itemset Z has `support(Z)`, already computed in the frequent-itemset phase. **No extra database scan is needed**; rule generation is pure arithmetic on numbers you already have.

**Confidence monotonicity:** for a fixed Z, `σ(Z)` is constant, so confidence rises as the antecedent grows (consequent shrinks). **Therefore if `X → Y` fails minconf, every rule with a smaller antecedent and a larger consequent also fails** — whole branches can be pruned, which is what keeps the output manageable.

## A4. Complete worked example on the `{A,B,C}` itemset

Frequent itemset `{A,B,C}` with `σ(A)=4, σ(B)=3, σ(C)=4, σ(AB)=2, σ(AC)=3, σ(BC)=3, σ(ABC)=2, N=5`, **minconf = 60 %.**

**Level 1 — one-item consequents:**

| Rule | Confidence = σ(ABC)/σ(antecedent) | ≥ 0.6? |
|---|---|---|
| AB → C | 2/2 = **1.00** | ✓ |
| AC → B | 2/3 = **0.67** | ✓ |
| BC → A | 2/3 = **0.67** | ✓ |

**Level 2 — two-item consequents:**

| Rule | Confidence | ≥ 0.6? |
|---|---|---|
| A → BC | 2/4 = **0.50** | ✗ (prune) |
| B → AC | 2/3 = **0.67** | ✓ |
| C → AB | 2/4 = **0.50** | ✗ (prune) |

**Strong rules:** `AB → C (1.00)`, `AC → B (0.67)`, `BC → A (0.67)`, `B → AC (0.67)`.

**Why the two failures matter:** `A → BC` and `C → AB` fail because A and C are the **popular** items (support 0.8), so conditioning on them carries little information. **A confident rule needs a specific (low-support) antecedent and a common consequent** — a sentence that earns marks.

## A5. Your page's worked example: `Bread Milk → Butter`

**Given (100 transactions):**

| Itemset | Support |
|---|---|
| Bread + Milk | 30 % (0.30) |
| Bread + Butter | 20 % (0.20) |
| Milk + Butter | 25 % (0.25) |
| Bread + Milk + Butter | 15 % (0.15) |
| Butter (alone) | 40 % (0.40) |

**Rule generation for `Bread Milk → Butter`:**

```
Support of the rule      = support(Bread, Milk, Butter) = 0.15   (15 %)
Confidence               = support(Bread, Milk, Butter) / support(Bread, Milk)
                         = 0.15 / 0.30 = 0.50                   (50 %)
Lift                     = support(Bread, Milk, Butter) / (support(Bread, Milk) × support(Butter))
                         = 0.15 / (0.30 × 0.40)
                         = 0.15 / 0.12 = 1.25
```

**Interpretation (write exactly this):** *confidence of 50 % means half of the customers who buy Bread and Milk also buy Butter; lift = 1.25 > 1 indicates a meaningful **positive** relationship — the combination raises the chance of buying butter by 25 % over chance.*

**The complete rule set from `{Bread, Milk, Butter}`** (useful practice — compute each one). Your page does not give the individual supports of Bread and Milk, so take **support(Bread) = 0.60** and **support(Milk) = 0.50**; state such an assumption explicitly in an exam.

| Rule | Confidence | Lift |
|---|---|---|
| Bread Milk → Butter | 0.15/0.30 = **0.50** | 0.15/(0.30×0.40) = **1.25** |
| Bread Butter → Milk | 0.15/0.20 = **0.75** | 0.15/(0.20×0.50) = **1.50** |
| Milk Butter → Bread | 0.15/0.25 = **0.60** | 0.15/(0.25×0.60) = **1.00** |
| Bread → Milk Butter | 0.15/0.60 = **0.25** | 0.15/(0.60×0.25) = **1.00** |
| Milk → Bread Butter | 0.15/0.50 = **0.30** | 0.15/(0.50×0.20) = **1.50** |
| Butter → Bread Milk | 0.15/0.40 = **0.375** | 0.15/(0.40×0.30) = **1.25** |

Two lessons visible in the table: the rules with a **single-item antecedent** have the lowest confidence (they must predict **two** items), and **lift is identical for a rule and its mirror image** — `Bread Milk → Butter` and `Butter → Bread Milk` are both 1.25; `Bread Butter → Milk` and `Milk → Bread Butter` are both 1.50. **Lift is symmetric, confidence is not.**

---

# PART B — INTERESTINGNESS MEASURES

## B1. Why interestingness measures are needed

**Not all rules with high confidence are truly meaningful**, so additional measures are needed. The three most commonly used are **support, confidence and lift**.

| Measure | What it measures | What it shows |
|---|---|---|
| **Support** | how frequently the rule occurs | a rule **must** meet minimum support to be considered |
| **Confidence** | how often the consequent appears when the antecedent is present | the **reliability** of the rule |
| **Lift** | how much more often X and Y occur together than if independent | **> 1** positive, **= 1** independent, **< 1** negative association |

## B2. Additional interestingness measures (your page's four)

**Leverage** — the **difference between the observed frequency of X and Y occurring together and the expected frequency under independence**:
```
leverage = P(X ∪ Y) − P(X)·P(Y)
```
A leverage **close to zero indicates independence** (positive → co-occur more than chance; negative → less).

**Conviction** — measures **how strongly the absence of Y is related to the presence of X**:
```
conviction = (1 − P(Y)) / (1 − confidence(X → Y))
```
**Higher conviction = stronger rule.** It equals 1 under independence and ∞ for a rule that is always right (confidence = 1). It is **asymmetric**, so it distinguishes `X → Y` from `Y → X` even when their lifts agree.

**Cosine similarity** — evaluates **how close the relationship between two items is, based on angle similarity**:
```
cosine = P(X ∪ Y) / √(P(X)·P(Y))
```
**Used for symmetric associations** (it does not favour either direction) and it is **null-invariant** — adding transactions that contain neither item does not change it.

**Jaccard measure** — the **ratio of the intersection over the union of item occurrences**:
```
jaccard = P(X ∪ Y) / (P(X) + P(Y) − P(X ∪ Y))
```
**Useful when analysing similarity between sets**; also symmetric and null-invariant.

*These measures help analysts choose rules that are **statistically meaningful and not just frequent**.*

## B3. The full measure table (for a numerical question)

For `X → Y` with `P(X)=0.8, P(Y)=0.6, P(X∪Y)=0.4`:

| Measure | Formula | Value | Verdict |
|---|---|---|---|
| Support | `P(X∪Y)` | 0.400 | frequent |
| Confidence | `P(X∪Y)/P(X)` | 0.500 | respectable |
| **Lift** | `P(X∪Y)/(P(X)P(Y))` | **0.833** | **negative association** |
| Leverage | `P(X∪Y) − P(X)P(Y)` | −0.080 | co-occur less than chance |
| Conviction | `(1−P(Y))/(1−conf)` | 0.800 | confirms negative |
| Cosine | `P(X∪Y)/√(P(X)P(Y))` | 0.577 | weak |
| Jaccard | `P(X∪Y)/(P(X)+P(Y)−P(X∪Y))` | 0.400 | weak |
| Kulczynski | `½[P(XY)/P(X) + P(XY)/P(Y)]` | 0.583 | weak |

**Every measure except support and confidence says this rule is not worth acting on** — the single most important point of the topic.

## B4. Which measure to use when

| Situation | Prefer |
|---|---|
| Retail cross-selling, balanced item frequencies | **lift** (simple, interpretable) |
| Need an absolute (not ratio) effect size | **leverage** |
| Direction matters, independence must equal 1 | **conviction** |
| Very imbalanced supports (rare items) | **null-invariant** measures: cosine, Jaccard, Kulczynski, all-confidence |
| Statistical rigour, significance testing | **χ²** with a p-value |
| Explaining to a business audience | **support + confidence + lift**, in that order |

**Null invariance (worth a sentence in a 10-mark answer):** a measure is null-invariant if its value does not change when transactions containing **neither** item are added. **Lift, leverage, conviction and χ² are not** null-invariant; **cosine, Jaccard, Kulczynski and all-confidence are** — which is why they are preferred for **cross-support** data (a 0.01 % item paired with a 50 % item).

---

# PART C — IMPORTANCE AND CHALLENGES

## C1. Why interestingness measures are necessary (your page's five reasons)

1. **Confidence alone can be misleading when the consequent is very frequent.**
2. **Lift** identifies whether the rule is **stronger than random chance**.
3. **Leverage** highlights **how much extra support** the rule has beyond independence.
4. **Conviction** helps judge **how strongly the rule predicts** the consequent.
5. They **prevent selecting rules that appear strong but have no practical significance**.

*These measures help analysts focus only on the most useful and actionable rules.*

## C2. Challenges in rule generation (your page's five)

| Challenge | Why it happens | Mitigation |
|---|---|---|
| A single frequent itemset can generate **many possible rules** | `2^k − 2` rules per k-itemset | confidence pruning; closed/maximal itemsets |
| **Low thresholds** produce **too many rules** | support and confidence both permissive | raise thresholds, constrain with templates |
| **Interpretation** is difficult | statistical strength ≠ business meaning | domain expert review, subjective interestingness |
| **Computational cost** rises rapidly | dataset size and item diversity | efficient measures, pruning, parallelism |
| Many rules are **redundant or uninteresting** | overlapping itemsets produce near-duplicates | non-redundant/minimal rule sets |

**Efficient evaluation using interestingness measures is crucial to manage these challenges.**

---

# PART D — ADVANCED POINTS (for the extra 2–3 marks)

## D1. Four classic failures of support + confidence

1. **The trivial rule** — `{Milk} → {Bread}` at 75 % confidence is unimpressive if 80 % of baskets already contain bread (lift < 1).
2. **Independence** — two items each bought 50 % of the time give a 50 %-confidence rule that says nothing (lift = 1).
3. **Cross-support patterns** — rare item X (0.1 %) and rare Y (0.1 %) occurring together in 0.09 % gives ~90 % confidence on a handful of transactions.
4. **Simpson's paradox** — a rule can hold overall yet reverse inside every subgroup (a confounder is hidden by aggregation).

## D2. Compact representations of the output

| Concept | Definition | Benefit |
|---|---|---|
| **Closed frequent itemset** | a frequent itemset with **no proper superset of the same support** | preserves all itemsets *and* their supports in far fewer entries |
| **Maximal frequent itemset** | a frequent itemset with **no frequent proper superset** | most compact; subset supports are only bounded, not known |
| **Non-redundant rule set** | rules not derivable from others | a human-sized output |

*Example:* if `{A,B}:3` and `{A,B,C}:3`, then `{A,B}` is **not closed**, and `{A,B,C}` is **both closed and maximal**. (A maximal itemset is always closed; the converse is false.)

## D3. Subjective interestingness

Objective measures cannot know what the analyst already knows. A pattern is subjectively interesting if it is **unexpected, actionable, novel, understandable and corroborated**. Systems therefore allow **meta-rule guided mining** — e.g. mine only rules whose antecedent contains a chosen product, or whose consequent is in a chosen category — which both shrinks the output and makes it relevant.

---

## D4. Summary paragraph

Rule generation turns each frequent itemset Z into rules `X → Z−X`, in six steps: take the frequent itemsets, list every non-empty subset, form the rule, compute `confidence = σ(Z)/σ(X)`, discard anything below minimum confidence, then filter the survivors with further interestingness measures. Because confidence rises as the antecedent grows, one failing rule prunes all weaker-antecedent variants, which is the only reason large itemsets are tractable (a k-itemset has `2^k − 2` rules). Support measures frequency, confidence measures reliability, and **lift** compares the rule against the consequent's base rate (1 = independent, > 1 positive, < 1 negative), with **leverage, conviction, cosine and Jaccard** available for direction, absolute effect and rare-item cases. The goal throughout is to move from rules that are merely *frequent and strong* to rules that are **statistically interesting and practically actionable**.

---
**End of notes.** Continue to the [revision cheat sheet](../exam/cheat-sheet.md) and the [question bank](../exam/question-bank.md).
