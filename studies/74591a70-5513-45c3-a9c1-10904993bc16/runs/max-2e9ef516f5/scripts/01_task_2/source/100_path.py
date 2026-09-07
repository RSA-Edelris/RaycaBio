
import json
from pathlib import Path

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
MMDIR = Path(BASE) / "mmgbsa"

with open(f"{BASE}/docking_scores_all32.json") as fh:
    dock = json.load(fh)
with open(f"{MMDIR}/mmgbsa_results.json") as fh:
    gbsa = json.load(fh)

rows = []
for name, ds in dock.items():
    dg_vina  = ds.get("affinity", float("nan"))
    cnn_pkd  = ds.get("cnn_affinity", float("nan"))
    gs       = gbsa.get(name, {})
    dg_gbsa  = gs.get("DELTA TOTAL", float("nan"))
    dg_std   = gs.get("DELTA TOTAL_std", float("nan"))
    vdw      = gs.get("VDWAALS", float("nan"))
    eel      = gs.get("EEL", float("nan"))
    egb      = gs.get("EGB", float("nan"))
    esurf    = gs.get("ESURF", float("nan"))
    rows.append(dict(name=name, vina_dg=dg_vina, cnn_pkd=cnn_pkd,
                     gbsa_dg=dg_gbsa, gbsa_std=dg_std,
                     vdwaals=vdw, eel=eel, egb=egb, esurf=esurf))

rows.sort(key=lambda r: r["gbsa_dg"] if r["gbsa_dg"] == r["gbsa_dg"] else 9999)

hdr = (f"{'Rank':>4}  {'Compound':<26}  {'Vina ΔG':>7}  {'CNN pKd':>7}  "
       f"{'GBSA ΔG':>9}  {'±':>5}  {'VDWAALS':>8}  {'EEL':>7}  {'EGB':>7}  {'ESURF':>6}")
print(hdr)
print("-" * len(hdr))
for i, r in enumerate(rows, 1):
    print(f"{i:>4}  {r['name']:<26}  {r['vina_dg']:>7.2f}  {r['cnn_pkd']:>7.2f}  "
          f"{r['gbsa_dg']:>9.2f}  {r['gbsa_std']:>5.2f}  "
          f"{r['vdwaals']:>8.2f}  {r['eel']:>7.2f}  {r['egb']:>7.2f}  {r['esurf']:>6.2f}")

print(f"\n32 compounds — sorted by MM-GBSA ΔG (kcal/mol)")

with open(f"{MMDIR}/combined_results.json", "w") as fh:
    json.dump({"ranked": rows}, fh, indent=2)
print("Saved combined_results.json")
