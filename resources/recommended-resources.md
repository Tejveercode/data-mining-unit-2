# Recommended Resources — best, alternatives, and the minimum set

Judged on: **coverage of this exact syllabus**, correctness, currency (2022–2026), and cost. Your LMS page lists Han and Tan as textbooks, so those two are the anchor; everything else fills the gaps they leave.

---

## THE ONE BEST (buy/borrow this)

### 1. Han, Pei & Tong — *Data Mining: Concepts and Techniques*, 4th edition (Morgan Kaufmann, 2022)
- **Latest edition** of the classic (3rd ed. was 2011 — the edition your LMS page still cites, so this is the upgrade).
- Chapters that matter for Unit 2: **Ch. 3 Data Preprocessing** (cleaning, integration, reduction, transformation, discretization) and **Ch. 6 Mining Frequent Patterns** (Apriori, FP-Growth, rule generation, interestingness, closed/maximal itemsets).
- **Why it wins:** it is the *only* book that covers every topic in your Unit 2 to the exact depth your questions ask, including the algorithms' pseudocode, and it is the source your LMS notes were written from — so the vocabulary matches your exam.
- Get it: <https://shop.elsevier.com/books/data-mining/han/978-0-12-811760-6>

---

## THE BEST FREE COMPANION (use alongside, not instead)

### 2. Tan, Steinbach, Karpatne & Kumar — *Introduction to Data Mining*, 2nd edition — official site
<https://www-users.cse.umn.edu/~kumar/dmbook/index.php>
- Chapter 2 (Data) is the clearest explanation of **aggregation, sampling, dimensionality reduction, feature subset selection, feature creation, discretization, variable transformation and similarity measures** anywhere — it is the *conceptual* counterpart to Han's algorithmic treatment.
- Free **lecture slides and exercises** on the site, which map 1:1 onto the topics in your Unit 2 Chapter 2.1/2.2.

---

## ALTERNATIVES (pick by what you need)

| Resource | Best for | Notes |
|---|---|---|
| **Witten, Frank, Hall, Pal & Foulds — *Data Mining: Practical ML Tools and Techniques*, 5th ed. (2025)** — <https://shop.elsevier.com/books/data-mining/witten/978-0-443-15888-9> | the *practical* view + WEKA | newest edition (2026 TAA "Texty" award); best if you want to actually run filters. Weakest on association-rule theory. |
| **Aggarwal — *Data Mining: The Textbook* (Springer, 2015)** — <https://link.springer.com/book/10.1007/978-3-319-14142-8> | deeper maths, modern data types | excellent on PCA/dimensionality; heavier than you need for Unit 2. |
| **Leskovec, Rajaraman & Ullman — *Mining of Massive Datasets*, 3rd ed. (free PDF)** — <http://mmds.org/> | sampling, hashing, scale, association rules at scale | free; the Stanford CS246 lectures (same site) are outstanding on frequent itemsets. |
| **NPTEL — Data Mining / Data Analytics courses (video)** | exam-style explanation in Indian-university framing | matches a CU/BCA-style exam better than a US lecture. |
| **scikit-learn user guide — preprocessing chapter** — <https://scikit-learn.org/stable/modules/preprocessing.html> | implementation of every transformation in this unit | the reference for `StandardScaler`, `MinMaxScaler`, `KBinsDiscretizer`, `SimpleImputer`, `OneHotEncoder`, `PCA`, `RFE`. |
| **GeeksforGeeks / Tutorialspoint (the two links on your LMS page)** | quick revision, definitions | useful for last-minute recall; occasionally imprecise — trust Han/Tan where they disagree. |

---

## THE MINIMUM SET (if you have one evening)

1. **This repository's** [notes](../notes/) — the syllabus in order, with worked numericals.
2. **Han Ch. 3 + Ch. 6.1–6.3** — read only the sections your LMS topics name.
3. **Tan Ch. 2 lecture slides** (free) — skim for the tables and the "why".
4. **scikit-learn preprocessing page** — so you can actually do it in code.

That is enough for a full-marks Unit 2.

---

## Study order that matches your LMS chapters

| Your LMS | Read this repo | Then in the textbook |
|---|---|---|
| Ch. 2.1 — introduction, cleaning, integration, reduction | notes 01–05 | Han §3.1–3.4 ; Tan Ch. 2 intro |
| Ch. 2.2 — sampling, subset selection, transformation, discretization, frequent patterns | notes 06–09 | Han §3.4–3.5, §6.1 ; Tan §2.3–2.4, Ch. 6.1 |
| Ch. 2.3 — Apriori, examples, FP-Growth, rule generation | notes 10–13 | Han §6.2–6.3 ; Tan Ch. 6.2–6.7 |

---

## Two cautions

- **The LMS page's own reference list is out of date** (Han 3rd ed. 2011, Witten 4th ed. 2016). The 4th edition of Han (2022) and the 5th of Witten (2025) are current; the chapter structure is unchanged, so page numbers differ but the content is the same or better.
- **Do not study association rules from video summaries alone.** The marks in Apriori/FP-Growth questions come from *doing the tables*; only practice produces that.
