
import json, pandas as pd, numpy as np, os, glob, time

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as fh:
    ligs = json.load(fh)
smiles_list    = [v["smiles"] for v in ligs.values()]
smiles_to_name = {v["smiles"]: k for k, v in ligs.items()}

# Timing probe: 5 high-priority accessions
probe = ["P24941","P49841","P00533","P00519","O14965"]  # CDK2,GSK3B,EGFR,ABL1,AURKA
t0 = time.time()
r  = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "accessions":       probe,
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_probe5",
})
elapsed = time.time() - t0
print(f"rc={r.get('returncode', r.get('rc','?'))}  elapsed={elapsed:.0f}s")
print(r.get("stdout","")[-500:])
