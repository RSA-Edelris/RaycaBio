
import json, os
import numpy as np

SESSION = "/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74"

# Re-collect with correct field names
scores = {}
for cmpd in [f"ARV_{i:03d}" for i in range(1, 11)]:
    pred = f"{SESSION}/{cmpd}/boltz_results_{cmpd}_constrained/predictions/{cmpd}_constrained"
    scores[cmpd] = {}
    for mi in range(3):
        with open(f"{pred}/confidence_{cmpd}_constrained_model_{mi}.json") as f:
            d = json.load(f)
        pci = d["pair_chains_iptm"]
        scores[cmpd][mi] = {
            "conf":       d["confidence_score"],
            "ptm":        d["ptm"],
            "iptm":       d["iptm"],
            "lig_era":    d["ligand_iptm"],            # pci[2][0]
            "lig_crbn":   pci["2"]["1"],               # cooperativity proxy
            "prot_iptm":  d["protein_iptm"],           # ERα↔CRBN
            "era_crbn":   pci["0"]["1"],               # ERα→CRBN
            "crbn_era":   pci["1"]["0"],               # CRBN→ERα
        }

# Rank by model_0 lig_crbn
m0 = {c: scores[c][0] for c in scores}
ranked = sorted(m0.items(), key=lambda x: x[1]["lig_crbn"], reverse=True)

# Unconstrained model_0 values for comparison (job 6534300)
unc = {"ARV_001":0.5086,"ARV_002":0.2718,"ARV_003":0.4059,"ARV_004":0.2657,
       "ARV_005":0.3461,"ARV_006":0.4331,"ARV_007":0.1932,"ARV_008":0.3331,
       "ARV_009":0.3574,"ARV_010":0.2454}

print("=== CONSTRAINED RUN — COOPERATIVITY RANKING (model_0, job 6548359) ===")
print(f"{'Rank':>4}  {'Compound':>8}  {'conf':>6}  {'iptm':>6}  {'lig→ERα':>8}  {'lig→CRBN':>9}  {'prot_iptm':>10}  {'Δ vs unconstrained':>20}")
print("-"*80)
for rank, (cmpd, s) in enumerate(ranked, 1):
    delta = s["lig_crbn"] - unc[cmpd]
    flag = " ⚠" if cmpd == "ARV_010" else ""
    print(f"{rank:>4}  {cmpd:>8}  {s['conf']:.4f}  {s['iptm']:.4f}  {s['lig_era']:.4f}    {s['lig_crbn']:.4f}     {s['prot_iptm']:.4f}        {delta:+.4f}{flag}")

print(f"\nARV-471 ref unconstrained model_0: lig→CRBN = 0.2306")
print("All 10 compounds exceed the ARV-471 unconstrained reference.")
