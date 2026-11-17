# Topic 4 — Data Integration: Schema Integration & Redundancy Removal

> **LMS page:** *Chapter 2.1 — Data Integration: Schema Integration, Redundancy Removal* · **CO2**

---

## 1. What data integration is

**Definition.** Data integration is the process of **combining data from multiple sources into a single, unified view**.

Organisations store the same business in many systems — an RDBMS, Excel sheets, CSV exports, application logs, external APIs, a data warehouse. Before mining, these must be merged into one structured, consistent dataset that is **complete, consistent, accurate and usable**.

Two major tasks: **schema integration** (make the structures agree) and **redundancy removal** (stop the same fact appearing twice).

**The three classic integration problems** (Han's list — worth naming):
1. **Schema integration** — different structures and names for the same thing.
2. **Redundancy** — the same attribute or record appears in several sources.
3. **Value conflicts** — different sources give different values for the same entity (e.g. age 25 vs 26).

---

## 2. Schema integration

**Definition.** Schema integration is the process of **merging attributes, tables or data structures from different sources into a single unified schema**. A schema defines how data is organised, named, typed and related.

When sources are combined, their schemas conflict; integration resolves those conflicts so the data can be used together without ambiguity.

### 2.1 Challenges in schema integration (six, from the LMS page)

| Conflict | Meaning | Example |
|---|---|---|
| **Naming conflict** | different names for the same attribute | `CustID` vs `Customer_ID` |
| **Synonym** | two names mean the same concept | `Salary` and `Pay` |
| **Homonym** | the **same name** means different things | `Name` = product name in one table, person name in another |
| **Data type conflict** | same information stored with different types | `Age` as integer in one table, string `"25"` in another |
| **Structural conflict** | data organised differently | address as one string vs split into `Street, City, State` |
| **Unit conflict** | different measurement units | weight in kilograms vs pounds |

Two more that appear in textbooks and impress in answers:
- **Granularity conflict** — one source stores per-day records, another per-month totals.
- **Value-encoding conflict** — `M/F` vs `0/1` vs `Male/Female`; `true/false` vs `Y/N`.

### 2.2 Techniques and steps in schema integration

1. **Schema matching** — identify which attributes refer to the same concept, using name similarity, metadata, descriptions, data profiling (do the value ranges match?) and domain knowledge.
2. **Attribute mapping** — write rules mapping attributes with different names but identical meaning (`Phone_Number` → `Contact_No`).
3. **Resolving naming conflicts** — rename to a standard convention; document the dictionary.
4. **Resolving structural conflicts** — split or merge attributes to fit the target schema (merge `first_name` + `last_name` into `full_name`, or the reverse).
5. **Data type conversion** — cast to a common type (`"25"` → `25`).
6. **Unit standardization** — convert to one measurement system (all weights to kg, all currency to INR) **before** merging.
7. **Schema merging** — build the unified schema that holds the integrated data.

Result: consistency, and no ambiguity about what a column means.

> **Practical tools:** ETL platforms (Informatica, Talend, Apache NiFi, dbt), SQL `JOIN` + `UNION`, pandas `merge`/`concat`, and schema-matching research tools. In an exam, describing the *logic* matters more than naming tools.

---

## 3. Redundancy

**Definition.** Redundancy occurs when **the same data appears multiple times** across sources. During integration, repeated data causes **inconsistencies, extra storage cost and distorted mining results** if not handled.

**Redundancy removal** is the process of identifying duplicate or overlapping data and keeping only unique, correct records.

### 3.1 Types of redundancy

| Type | Meaning | Example |
|---|---|---|
| **Attribute redundancy** | the same information stored in two or more attributes | `Age` and `Date_of_Birth` — age is derivable from DOB |
| **Tuple / record redundancy** | the same entity stored multiple times, possibly across sources | a customer in both the CRM and the billing database |

### 3.2 How redundancy occurs
- Multiple systems storing similar data (no single source of truth).
- Duplicate data entry by different departments.
- Merging historical data with current data.
- Data arriving from third-party sources.
- Schema differences producing partial duplicates (one source has the address, another the phone).

### 3.3 Detecting redundancy — the statistical tests (a favourite exam question)

**Numeric vs numeric → correlation coefficient.**
```
r(A,B) = Σ(aᵢ − Ā)(bᵢ − B̄) / ((n−1)·σ_A·σ_B)
```
- `r > 0` : A and B rise together (positive correlation); `r < 0` : one rises as the other falls.
- `|r| > 0.9` (a common rule of thumb) → **strong redundancy**; one of the attributes can often be dropped.
- `r ≈ 0` → no linear relationship (but a **non-linear** relationship can still exist — check a scatter plot).

**Covariance** is the un-normalised version: `Cov(A,B) = Σ(aᵢ − Ā)(bᵢ − B̄)/(n−1)`. Sign shows direction, magnitude is unit-dependent, which is why we prefer `r`.

**Nominal vs nominal → χ² (chi-square) test of independence.**
```
χ² = Σ (observed − expected)² / expected
```
where `expected = (row total × column total) / grand total`. A large χ² (compared with the critical value for `(r−1)(c−1)` degrees of freedom) means the two nominal attributes are **dependent → redundant**.

*Small example.* Gender vs Product preference:

| | Product A | Product B | Total |
|---|---|---|---|
| Male | 30 | 10 | 40 |
| Female | 10 | 30 | 40 |
| Total | 40 | 40 | 80 |

Expected: Male/A = 40×40/80 = 20; Male/B = 20; Female/A = 20; Female/B = 20.
χ² = (30−20)²/20 + (10−20)²/20 + (10−20)²/20 + (30−20)²/20 = 5 + 5 + 5 + 5 = **20**.
With 1 degree of freedom, χ² = 20 ≫ 3.84 (5 % critical value) → strongly dependent → redundant.

**Numeric vs nominal → ANOVA / correlation ratio (η).** Tests whether the mean of the numeric attribute differs across the categories of the nominal one.

**Duplicate records** are found by **record linkage / entity resolution**: primary or composite keys first; then **string similarity** (edit distance, Jaro–Winkler), **phonetic matching** (Soundex, Metaphone — catches "Jon"/"John"), **token-based similarity** (Jaccard on name tokens), and probabilistic matching (Fellegi–Sunter). **Blocking** (compare only records sharing a key such as pincode + surname) keeps the comparison count manageable.

---

## 4. Techniques for redundancy removal (LMS list)

1. **Duplicate record detection** — compare on primary keys, composite keys or unique identifiers.
2. **Record linkage** — match records referring to the same entity even when identifiers differ (string similarity, phonetic, probabilistic).
3. **Merge and consolidation** — combine duplicates into one record holding the **most accurate** value per field (survivorship rules).
4. **Attribute elimination** — remove attributes that duplicate information or can be derived from others (`Age` from `Date_of_Birth`).
5. **Functional dependency analysis** — if `Zip_Code → City`, storing both is redundant; keep the determinant.
6. **Conflict resolution** — when two sources disagree, choose based on business rules, recency, completeness or source credibility (a "trust score").
7. **Standardization** — uniform formatting (`Jon`/`John`, `+91-98…`/`098…`) makes duplicates detectable in the first place.

---

## 5. Benefits of schema integration and redundancy removal

- Produces a **consistent, unified dataset** for analysis.
- Eliminates confusion from **ambiguous attribute names**.
- **Reduces storage** by removing unnecessary duplicates.
- **Improves mining accuracy** (duplicates would double-count support and skew every average).
- Makes the integrated data **trustworthy and meaningful**.
- **Improves performance** by avoiding repeated processing.
- **Simplifies maintenance** and future updates.

---

## 6. Worked example (LMS example, expanded)

Two sources:

**Source 1:** `Customer_ID, Name, Age, City`
**Source 2:** `CustID, FullName, Date_of_Birth, Location`

Integration steps:
1. **Schema matching:** `Customer_ID = CustID`, `Name = FullName`, `City = Location`.
2. **Structural conflict:** Source 2 has `Date_of_Birth` where Source 1 has `Age` — convert one to the other (compute `Age` from DOB at a fixed reference date).
3. **Redundancy removal:** `Age` is derivable from `Date_of_Birth` → keep **one** (keep DOB: it is stable and does not go stale).
4. **Standardization:** unify city spellings (`Delhi`/`New Delhi`/`DL` → `Delhi`), trim names, normalise case.
5. **Merge records:** union of the two tables, deduplicated by customer name + city (+ phone if available).
6. **Conflict resolution:** if the two sources disagree on city, prefer the more recently updated source and log the conflict.

Final dataset: one row per customer, consistent fields, no derived duplicates.

---

## 7. Summary paragraph

Data integration builds one dataset out of many sources, and it has two halves. **Schema integration** resolves naming conflicts, synonyms, homonyms, type, structural and unit conflicts through schema matching, attribute mapping, conversion and standardisation, producing one unambiguous unified schema. **Redundancy removal** eliminates attribute redundancy (detected with correlation, χ² or ANOVA) and tuple redundancy (detected with record linkage — keys, string similarity, phonetic matching — then merged with survivorship rules and conflict resolution). Skip it and every downstream statistic is inflated by double counting; do it and the mining algorithm finally sees one consistent, trustworthy version of the truth.

---
**Next:** [Topic 5 — Data Reduction: Data Cube Aggregation & Dimensionality Reduction](05-data-reduction-cube-dimensionality.md)
