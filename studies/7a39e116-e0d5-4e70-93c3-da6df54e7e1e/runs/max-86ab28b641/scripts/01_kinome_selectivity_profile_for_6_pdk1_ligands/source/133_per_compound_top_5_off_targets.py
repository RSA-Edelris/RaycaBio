
# ── Per-compound top-5 off-targets ───────────────────────────────────────────
print("=== Per-compound top-5 off-targets (pIC50, excluding PDK1) ===\n")
for cpd in compounds:
    row = pivot.loc[cpd].drop("PDK1").sort_values(ascending=False)
    print(f"{cpd}  (PDK1={pivot.loc[cpd,'PDK1']:.2f})")
    for kin, val in row.head(5).items():
        delta = val - pivot.loc[cpd,"PDK1"]
        print(f"  {kin:<12} {val:.2f}  (Δ={delta:+.2f})")
    print()

# ── Common off-targets: hit at ≥6.90 in ALL 6 compounds ──────────────────────
threshold = 6.90
common = {}
for kin in pivot.columns:
    if kin == "PDK1": continue
    scores = pivot[kin].dropna()
    if len(scores) == len(compounds) and scores.min() >= threshold:
        common[kin] = scores.mean()
print(f"\n=== Common off-targets (pIC50 ≥{threshold} in ALL 6 compounds) ===")
for kin, m in sorted(common.items(), key=lambda x: -x[1]):
    print(f"  {kin:<12} mean={m:.2f}  family={FAMILY.get(kin,'?')}")

# ── Compound-specific: highest std and ≥1 compound clearly above threshold ───
spec_threshold = 7.05
specific = {}
for kin in pivot.columns:
    if kin == "PDK1": continue
    scores = pivot[kin].dropna()
    if scores.max() >= spec_threshold and scores.std() >= 0.12:
        specific[kin] = {"max": scores.max(), "std": scores.std(),
                         "top_cpd": pivot[kin].idxmax()}
print(f"\n=== Compound-specific off-targets (max≥{spec_threshold}, std≥0.12) ===")
for kin, d in sorted(specific.items(), key=lambda x: -x[1]["max"]):
    print(f"  {kin:<12} max={d['max']:.2f}  std={d['std']:.3f}  "
          f"top_cpd={d['top_cpd']}  family={FAMILY.get(kin,'?')}")
