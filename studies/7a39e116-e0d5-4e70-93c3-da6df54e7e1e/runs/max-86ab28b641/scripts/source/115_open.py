
import json, os

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as f:
    ligs = json.load(f)

names       = list(ligs.keys())
smiles_list = [v["smiles"] for v in ligs.values()]

print("Ligands:", names)

result_agc = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "kinase_families":  ["AGC"],
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_AGC",
})
print("AGC rc =", result_agc.get("rc"))
print("    n  =", result_agc.get("n_predictions"))
print("    csv=", result_agc.get("results_csv"))
print("    summary:", result_agc.get("summary","")[:600])
