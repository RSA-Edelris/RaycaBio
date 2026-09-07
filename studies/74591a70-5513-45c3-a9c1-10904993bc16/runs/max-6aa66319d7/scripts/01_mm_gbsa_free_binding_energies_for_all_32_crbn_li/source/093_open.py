
collation_script = r'''#!/usr/bin/env python3
"""
Collate docking scores + MM-GBSA results into a ranked table.
Run after run_mmpbsa.py has completed.
"""
import json
from pathlib import Path

WORK  = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
MMDIR = f"{WORK}/mmgbsa"

# Load docking scores
with open(f"{WORK}/docking_scores_all32.json") as fh:
    dock = json.load(fh)

# Load MM-GBSA results
mmgbsa_file = f"{MMDIR}/mmgbsa_results.json"
with open(mmgbsa_file) as fh:
    gbsa = json.load(fh)

# Build combined table
rows = []
for name, ds in dock.items():
    dg_vina = ds.get("vina_affinity", float("nan"))
    cnn_pkd = ds.get("cnn_affinity", float("nan"))
    cnn_pose = ds.get("cnn_pose_score", float("nan"))
    gs = gbsa.get(name, {})
    dg_gbsa  = gs.get("DELTA TOTAL", float("nan"))
    dg_std   = gs.get("DELTA TOTAL_std", float("nan"))
    vdw      = gs.get("VDWAALS", float("nan"))
    eel      = gs.get("EEL", float("nan"))
    egb      = gs.get("EGB", float("nan"))
    esurf    = gs.get("ESURF", float("nan"))
    rows.append({
        "name": name,
        "vina_dg": dg_vina,
        "cnn_pkd": cnn_pkd,
        "cnn_pose": cnn_pose,
        "gbsa_dg": dg_gbsa,
        "gbsa_std": dg_std,
        "vdwaals": vdw,
        "eel": eel,
        "egb": egb,
        "esurf": esurf,
    })

# Sort by MM-GBSA ΔG (most negative first); NaN goes last
rows.sort(key=lambda r: r["gbsa_dg"] if not (r["gbsa_dg"] != r["gbsa_dg"]) else 9999)

# Print table
hdr = (f"{'Rank':>4}  {'Compound':<26}  {'Vina':>6}  {'CNN pKd':>7}  "
       f"{'GBSA ΔG':>9}  {'±':>5}  {'VDWAALS':>8}  {'EEL':>7}  {'EGB':>7}  {'ESURF':>6}")
print(hdr)
print("-" * len(hdr))
for i, r in enumerate(rows, 1):
    has_gbsa = r["gbsa_dg"] == r["gbsa_dg"]  # not NaN
    gbsa_str = f"{r['gbsa_dg']:>9.2f}" if has_gbsa else "     N/A"
    std_str  = f"{r['gbsa_std']:>5.2f}" if has_gbsa else "   N/A"
    vdw_str  = f"{r['vdwaals']:>8.2f}" if has_gbsa else "     N/A"
    eel_str  = f"{r['eel']:>7.2f}" if has_gbsa else "    N/A"
    egb_str  = f"{r['egb']:>7.2f}" if has_gbsa else "    N/A"
    esurf_str= f"{r['esurf']:>6.2f}" if has_gbsa else "   N/A"
    print(f"{i:>4}  {r['name']:<26}  {r['vina_dg']:>6.2f}  {r['cnn_pkd']:>7.2f}  "
          f"{gbsa_str}  {std_str}  {vdw_str}  {eel_str}  {egb_str}  {esurf_str}")

print(f"\nTotal: {len(rows)} compounds  |  MM-GBSA available: {sum(1 for r in rows if r['gbsa_dg']==r['gbsa_dg'])}")

# Save as JSON
out = {"ranked": rows}
with open(f"{MMDIR}/combined_results.json", "w") as fh:
    json.dump(out, fh, indent=2)
print(f"Saved to {MMDIR}/combined_results.json")
'''

with open(f"{MMDIR}/collate_results.py", "w") as fh:
    fh.write(collation_script)
print("collate_results.py written")
print("\nPipeline readiness summary:")
print("  ✓ 32/32 antechamber (Gasteiger charges)")
print("  ✓ 32/32 tleap topologies (ff14SB + GAFF2)")
print("  ✓ LUMI job 21779205 running (32 parallel sander min+MD, rgbmax=12)")
print("  ✓ MMPBSA.py tested and working locally")
print("  ✓ run_mmpbsa.py ready (AMBERHOME, -cp, abs paths, DELTA TOTAL parse)")
print("  ✓ collate_results.py ready")
print("\nWaiting for LUMI job to complete (~1-2 hr remaining).")
