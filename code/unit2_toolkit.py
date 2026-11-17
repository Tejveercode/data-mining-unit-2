#!/usr/bin/env python3
"""
Unit 2 toolkit — every technique from the syllabus, implemented in plain Python.

No third-party packages: run it anywhere.

    python unit2_toolkit.py            # runs all demos
    python unit2_toolkit.py apriori    # runs one demo

Sections
  1. cleaning        missing values, IQR/z-score outliers, binning, moving average
  2. integration     correlation and chi-square redundancy checks
  3. reduction       sampling (random/stratified/systematic/reservoir)
  4. transformation  min-max, z-score, decimal scaling, log, robust; one-hot/ordinal
  5. discretization  equal-width, equal-frequency, entropy (information gain)
  6. association     Apriori, FP-tree construction, rule generation, lift/leverage/conviction
"""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict


# ----------------------------------------------------------------------------
# 1. CLEANING
# ----------------------------------------------------------------------------
def impute(values, method="median"):
    """Impute None values. method: mean | median | mode."""
    known = [v for v in values if v is not None]
    if not known:
        return values[:]
    if method == "mean":
        fill = sum(known) / len(known)
    elif method == "mode":
        fill = Counter(known).most_common(1)[0][0]
    else:  # median
        s = sorted(known)
        n = len(s)
        fill = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    return [fill if v is None else v for v in values]


def outliers_iqr(values):
    """Return (lower, upper, [outliers]) using the 1.5*IQR rule."""
    s = sorted(values)
    n = len(s)
    q1 = s[n // 4]
    q3 = s[(3 * n) // 4]
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return lo, hi, [v for v in values if v < lo or v > hi]


def outliers_zscore(values, threshold=3.0):
    """Return (mean, sd, [outliers]) using |z| > threshold."""
    n = len(values)
    mu = sum(values) / n
    sd = math.sqrt(sum((v - mu) ** 2 for v in values) / (n - 1)) if n > 1 else 0.0
    if sd == 0:
        return mu, sd, []
    return mu, sd, [v for v in values if abs((v - mu) / sd) > threshold]


def bin_smooth(values, k=3, how="mean"):
    """Equal-frequency binning. how: mean | median | boundary."""
    s = sorted(values)
    size = math.ceil(len(s) / k)
    out = []
    for i in range(0, len(s), size):
        b = s[i:i + size]
        if how == "mean":
            rep = sum(b) / len(b)
            out += [round(rep, 3)] * len(b)
        elif how == "median":
            m = len(b) // 2
            rep = b[m] if len(b) % 2 else (b[m - 1] + b[m]) / 2
            out += [round(rep, 3)] * len(b)
        else:  # boundary: snap to nearest bin min / max
            lo, hi = b[0], b[-1]
            out += [lo if (v - lo) <= (hi - v) else hi for v in b]
    return out


def moving_average(values, window=3):
    """Trailing moving average of the given window."""
    out = []
    for i in range(len(values)):
        lo = max(0, i - window + 1)
        chunk = values[lo:i + 1]
        out.append(round(sum(chunk) / len(chunk), 3))
    return out


# ----------------------------------------------------------------------------
# 2. INTEGRATION (redundancy detection)
# ----------------------------------------------------------------------------
def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return num / (da * db) if da and db else 0.0


def chi_square(table):
    """table: list of rows of observed counts. Returns (chi2, dof)."""
    rows = len(table)
    cols = len(table[0])
    row_tot = [sum(r) for r in table]
    col_tot = [sum(table[r][c] for r in range(rows)) for c in range(cols)]
    grand = sum(row_tot)
    chi2 = 0.0
    for r in range(rows):
        for c in range(cols):
            exp = row_tot[r] * col_tot[c] / grand
            if exp:
                chi2 += (table[r][c] - exp) ** 2 / exp
    return chi2, (rows - 1) * (cols - 1)


# ----------------------------------------------------------------------------
# 3. REDUCTION (sampling)
# ----------------------------------------------------------------------------
def sample_random(data, n, seed=0):
    return random.Random(seed).sample(data, n)


def sample_stratified(data, label_of, n, seed=0):
    """Proportional allocation across the groups returned by label_of."""
    rnd = random.Random(seed)
    groups = defaultdict(list)
    for row in data:
        groups[label_of(row)].append(row)
    out = []
    for rows in groups.values():
        take = max(1, round(n * len(rows) / len(data)))
        out += rnd.sample(rows, min(take, len(rows)))
    return out


def sample_systematic(data, n):
    k = max(1, len(data) // n)
    start = random.randrange(k)
    return data[start::k][:n]


def sample_reservoir(stream, k, seed=0):
    """Uniform sample of k items from a stream of unknown length."""
    rnd = random.Random(seed)
    res = []
    for i, item in enumerate(stream):
        if i < k:
            res.append(item)
        else:
            j = rnd.randint(0, i)
            if j < k:
                res[j] = item
    return res


# ----------------------------------------------------------------------------
# 4. TRANSFORMATION
# ----------------------------------------------------------------------------
def min_max(values, lo=0.0, hi=1.0):
    a, b = min(values), max(values)
    if a == b:
        return [lo] * len(values)
    return [round(lo + (v - a) * (hi - lo) / (b - a), 4) for v in values]


def z_score(values):
    n = len(values)
    mu = sum(values) / n
    sd = math.sqrt(sum((v - mu) ** 2 for v in values) / (n - 1)) if n > 1 else 1.0
    return [round((v - mu) / sd, 4) for v in values]


def decimal_scale(values):
    j = 0
    while max(abs(v) for v in values) / (10 ** j) >= 1:
        j += 1
    return [round(v / 10 ** j, 6) for v in values], j


def log_transform(values):
    return [round(math.log1p(v), 4) for v in values]


def robust_scale(values):
    s = sorted(values)
    n = len(s)
    med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    q1, q3 = s[n // 4], s[(3 * n) // 4]
    iqr = (q3 - q1) or 1
    return [round((v - med) / iqr, 4) for v in values]


def one_hot(categories):
    levels = sorted(set(categories))
    return levels, [[1 if c == lv else 0 for lv in levels] for c in categories]


def ordinal_encode(values, order):
    mapping = {v: i + 1 for i, v in enumerate(order)}
    return mapping, [mapping[v] for v in values]


# ----------------------------------------------------------------------------
# 5. DISCRETIZATION
# ----------------------------------------------------------------------------
def equal_width(values, k=3):
    a, b = min(values), max(values)
    w = (b - a) / k
    edges = [a + i * w for i in range(k + 1)]
    out = []
    for v in values:
        idx = min(int((v - a) / w) if w else 0, k - 1)
        out.append(idx)
    return edges, out


def equal_frequency(values, k=3):
    """Equal-frequency (equal-depth) bins: ceil(n/k) values per bin."""
    s = sorted(values)
    size = math.ceil(len(s) / k)
    # boundary of bin i = the last value that still belongs to bin i
    edges = [s[0]]
    for i in range(1, k):
        last = min(i * size - 1, len(s) - 1)
        edges.append(s[last])
    edges.append(s[-1])
    codes = []
    for v in values:
        pos = s.index(v)                       # position in the sorted order
        codes.append(min(pos // size, k - 1))
    return edges, codes


def entropy(counts):
    total = sum(counts)
    return -sum((c / total) * math.log2(c / total) for c in counts if c)


def best_entropy_split(pairs):
    """pairs: list of (value, label). Returns (best_threshold, gain)."""
    pairs = sorted(pairs)
    labels = [p[1] for p in pairs]
    base = entropy(list(Counter(labels).values()))
    values = [p[0] for p in pairs]
    best_t, best_gain = None, 0.0
    for i in range(len(pairs) - 1):
        if values[i] == values[i + 1]:
            continue
        t = (values[i] + values[i + 1]) / 2
        left = [l for v, l in pairs if v <= t]
        right = [l for v, l in pairs if v > t]
        w = (len(left) / len(pairs)) * entropy(list(Counter(left).values()))
        w += (len(right) / len(pairs)) * entropy(list(Counter(right).values()))
        gain = base - w
        if gain > best_gain:
            best_t, best_gain = t, gain
    return best_t, round(best_gain, 4)


# ----------------------------------------------------------------------------
# 6. ASSOCIATION RULES
# ----------------------------------------------------------------------------
def _subsets(s, size):
    s = list(s)
    if size == 0:
        yield ()
        return
    for i in range(len(s)):
        for rest in _subsets(s[i + 1:], size - 1):
            yield (s[i],) + rest


def apriori(transactions, min_support=0.4):
    """Return (frequent_itemsets dict, level tables) for the given min_support fraction."""
    n = len(transactions)
    min_count = math.ceil(min_support * n)
    sets = [frozenset(t) for t in transactions]

    counts = Counter(i for s in sets for i in s)
    L = {frozenset([i]): c for i, c in counts.items() if c >= min_count}
    levels = [dict(L)]

    k = 2
    while L:
        items = sorted(L)
        cand = set()
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                union = items[i] | items[j]
                if len(union) == k:
                    # prune: every (k-1)-subset must be frequent
                    if all(frozenset(sub) in L for sub in _subsets(union, k - 1)):
                        cand.add(union)
        if not cand:
            break
        nxt = {}
        for c in cand:
            cnt = sum(1 for s in sets if c <= s)
            if cnt >= min_count:
                nxt[c] = cnt
        if not nxt:
            break
        levels.append(nxt)
        L = nxt
        k += 1

    frequent = {}
    for lvl in levels:
        frequent.update(lvl)
    return frequent, levels


def rules_from(frequent, n_transactions, min_conf=0.6):
    """Generate association rules with support, confidence, lift, leverage, conviction."""
    rules = []
    for z, count in frequent.items():
        if len(z) < 2:
            continue
        for r in range(1, len(z)):
            for ante_t in _subsets(sorted(z), r):
                ante = frozenset(ante_t)
                cons = z - ante
                s_xy = count / n_transactions
                s_x = frequent.get(ante, 0) / n_transactions
                s_y = frequent.get(cons, 0) / n_transactions
                if not s_x or not s_y:
                    continue
                conf = s_xy / s_x
                if conf >= min_conf:
                    rules.append({
                        "rule": f"{sorted(ante)} -> {sorted(cons)}",
                        "support": round(s_xy, 4),
                        "confidence": round(conf, 4),
                        "lift": round(s_xy / (s_x * s_y), 4),
                        "leverage": round(s_xy - s_x * s_y, 4),
                        "conviction": round((1 - s_y) / (1 - conf), 4) if conf < 1 else float("inf"),
                    })
    return sorted(rules, key=lambda d: -d["confidence"])


class FPNode:
    __slots__ = ("item", "count", "parent", "children", "link")

    def __init__(self, item, parent):
        self.item = item
        self.count = 0
        self.parent = parent
        self.children = {}
        self.link = None


def build_fp_tree(transactions, min_support=0.4):
    """Two scans: count items, then insert frequency-ordered paths. Returns (root, header, order)."""
    n = len(transactions)
    min_count = math.ceil(min_support * n)
    counts = Counter(i for t in transactions for i in t)
    freq = {i: c for i, c in counts.items() if c >= min_count}
    order = [i for i, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))]

    root = FPNode(None, None)
    header = {i: [freq[i], None] for i in order}
    for t in transactions:
        items = [i for i in order if i in t]
        node = root
        for it in items:
            if it in node.children:
                node = node.children[it]      # shared prefix: reuse, count only
                node.count += 1
                continue
            # new node -> create it AND thread it into the header chain exactly once
            child = FPNode(it, node)
            child.count = 1
            node.children[it] = child
            node = child
            if header[it][1] is None:
                header[it][1] = child
            else:
                p = header[it][1]
                while p.link is not None:
                    p = p.link
                p.link = child
    return root, header, order


def tree_as_paths(root, prefix=()):
    """Flatten the tree into (path tuple, count) leaves — handy for printing."""
    if not root.children:
        return [(" ".join(prefix) or "(root)", root.count)]
    out = []
    for item, child in root.children.items():
        out += tree_as_paths(child, prefix + (f"{item}:{child.count}",))
    return out


# ----------------------------------------------------------------------------
# DEMOS
# ----------------------------------------------------------------------------
def demo_cleaning():
    print("\n=== 1. CLEANING ===")
    ages = [25, None, 250, 30, 25, 41, None, 33]
    print("raw           :", ages)
    print("impute median :", impute(ages, "median"))
    print("impute mean   :", [round(v, 2) for v in impute(ages, "mean")])
    clean = [v for v in ages if v is not None]
    lo, hi, out = outliers_iqr(clean)
    print(f"IQR bounds    : [{lo}, {hi}]  outliers -> {out}")
    mu, sd, zout = outliers_zscore(clean)
    print(f"z-score       : mean={mu:.1f} sd={sd:.1f} outliers -> {zout or 'none found'}")
    print("                (teaching point: 250 inflates sd to 89.7, so |z| never exceeds 3")
    print("                 -> z-score hides its own outlier on skewed data; IQR catches it)")
    vals = [4, 8, 9, 15, 21, 21, 24, 25, 28, 34]
    print("bin mean      :", bin_smooth(vals, 3, "mean"))
    print("bin median    :", bin_smooth(vals, 3, "median"))
    print("bin boundary  :", bin_smooth(vals, 3, "boundary"))
    print("moving avg(3) :", moving_average([12, 14, 13, 12, 15, 95, 13, 14, 12, 13]))


def demo_integration():
    print("\n=== 2. INTEGRATION ===")
    height_cm = [160, 165, 170, 175, 180]
    height_m = [1.60, 1.65, 1.70, 1.75, 1.80]
    print(f"corr(height_cm, height_m) = {pearson(height_cm, height_m):.4f}  -> redundant")
    chi2, dof = chi_square([[30, 10], [10, 30]])
    print(f"chi2 = {chi2:.2f}, dof = {dof}  (critical 3.84 at 5%) -> dependent/redundant")


def demo_reduction():
    print("\n=== 3. REDUCTION ===")
    rows = [{"id": i, "cls": "A" if i % 3 else "B"} for i in range(30)]
    print("random 5      :", [r["id"] for r in sample_random(rows, 5)])
    print("stratified 6  :", [(r["id"], r["cls"]) for r in
                              sample_stratified(rows, lambda r: r["cls"], 6)])
    print("systematic 6  :", [r["id"] for r in sample_systematic(rows, 6)])
    print("reservoir 5   :", sample_reservoir([r["id"] for r in rows], 5))


def demo_transformation():
    print("\n=== 4. TRANSFORMATION ===")
    salary = [30000, 60000, 120000]
    print("raw           :", salary)
    print("min-max       :", min_max(salary))
    print("z-score       :", z_score(salary))
    scaled, j = decimal_scale(salary)
    print(f"decimal (j={j})  :", scaled)
    print("log           :", log_transform(salary))
    print("robust        :", robust_scale([10, 12, 13, 15, 100]))
    levels, oh = one_hot(["Delhi", "Mumbai", "Delhi"])
    print("one-hot", levels, ":", oh)
    mapping, enc = ordinal_encode(["Graduate", "Post Graduate", "High School"],
                                  ["High School", "Graduate", "Post Graduate"])
    print("ordinal", mapping, ":", enc)


def demo_discretization():
    print("\n=== 5. DISCRETIZATION ===")
    ages = [5, 12, 18, 25, 31, 40, 47, 55, 63, 70]
    e, codes = equal_width(ages, 3)
    print("equal-width edges :", [round(x, 2) for x in e], "codes:", codes)
    e, codes = equal_frequency(ages, 3)
    print("equal-freq edges  :", e, "codes:", codes)
    pairs = [(18, "N"), (20, "N"), (22, "Y"), (25, "Y"), (30, "Y"),
             (35, "N"), (40, "N"), (45, "Y"), (50, "Y"), (55, "Y")]
    t, gain = best_entropy_split(pairs)
    print(f"best entropy split at {t} with information gain {gain}")


def demo_association():
    print("\n=== 6. ASSOCIATION RULES ===")
    tx = [{"A", "B", "C"}, {"A", "C"}, {"A", "D"}, {"B", "C"}, {"A", "B", "C"}]
    print("transactions:", ["".join(sorted(t)) for t in tx])
    frequent, levels = apriori(tx, min_support=0.4)
    for k, lvl in enumerate(levels, start=1):
        print(f"  L{k}: " + ", ".join(f"{''.join(sorted(s))}:{c}" for s, c in
                                     sorted(lvl.items(), key=lambda kv: sorted(kv[0]))))
    print("  frequent itemsets:", len(frequent))

    print("\n  rules (min_conf = 0.6):")
    for r in rules_from(frequent, len(tx), 0.6):
        print(f"    {r['rule']:18s} sup={r['support']:.2f} conf={r['confidence']:.2f} "
              f"lift={r['lift']:.2f} lev={r['leverage']:+.2f} conv={r['conviction']:.2f}")

    root, header, order = build_fp_tree(tx, 0.4)
    print("\n  FP-tree order:", order)
    print("  header table :", {k: v[0] for k, v in header.items()})
    print("  tree branches:")
    for p in tree_as_paths(root):
        print("   ", p)


DEMOS = {
    "cleaning": demo_cleaning,
    "integration": demo_integration,
    "reduction": demo_reduction,
    "transformation": demo_transformation,
    "discretization": demo_discretization,
    "apriori": demo_association,
}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        DEMOS[sys.argv[1]]()
    else:
        for fn in DEMOS.values():
            fn()
