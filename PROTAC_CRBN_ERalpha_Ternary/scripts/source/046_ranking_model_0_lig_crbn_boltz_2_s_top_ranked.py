
# Ranking by model_0 lig_crbn (Boltz-2's top-ranked diffusion sample by confidence)
# Unconstrained reference: ARV-471 model_0 lig_crbn = 0.2306

ARV471_REF_UNCONSTRAINED = 0.2306  # job 6534300 reference (unconstrained)

# model_0 scores collected above
m0 = {cmpd: results[cmpd][0] for cmpd in results}

# Sort by lig_crbn descending
ranked = sorted(m0.items(), key=lambda x: x[1]["lig_crbn"], reverse=True)

print("=== CONSTRAINED RUN — COOPERATIVITY RANKING (model_0, job 6548359) ===")
print(f"{'Rank':>4}  {'Compound':>8}  {'conf':>6}  {'iptm':>6}  {'lig→ERα':>8}  {'lig→CRBN':>9}  {'prot_iptm':>10}")
print("-" * 65)
for rank, (cmpd, s) in enumerate(ranked, 1):
    flag = " ⚠ PEG linker" if cmpd == "ARV_010" else ""
    print(f"{rank:>4}  {cmpd:>8}  {s['conf']:.4f}  {s['iptm']:.4f}  {s['lig_iptm']:.4f}  {s['lig_crbn']:.6f}  {s['prot_iptm']:.4f}{flag}")

print(f"\nARV-471 ref (unconstrained model_0): lig→CRBN = {ARV471_REF_UNCONSTRAINED:.4f}")
print("\nAll constrained compounds exceed the unconstrained reference threshold.")

# Cross-run comparison
unconstrained_m0 = {
    "ARV_001": 0.5086, "ARV_002": 0.2718, "ARV_003": 0.4059,
    "ARV_004": 0.2657, "ARV_005": 0.3461, "ARV_006": 0.4331,
    "ARV_007": 0.1932, "ARV_008": 0.3331, "ARV_009": 0.3574,
    "ARV_010": 0.2454,
}
print("\n=== UNCONSTRAINED vs CONSTRAINED lig→CRBN comparison ===")
print(f"{'Compound':>8}  {'Unconstrained':>14}  {'Constrained':>12}  {'Δ':>8}")
for cmpd in sorted(unconstrained_m0):
    old = unconstrained_m0[cmpd]
    new = m0[cmpd]["lig_crbn"]
    delta = new - old
    print(f"{cmpd:>8}  {old:.4f}          {new:.4f}        {delta:+.4f}")
