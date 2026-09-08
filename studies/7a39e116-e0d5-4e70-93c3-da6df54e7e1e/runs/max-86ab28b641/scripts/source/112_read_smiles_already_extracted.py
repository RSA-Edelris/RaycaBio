
# Read the SMILES we already extracted
import json

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as f:
    ligs = json.load(f)

smiles_list = [v["smiles"] for v in ligs.values()]
names       = list(ligs.keys())

print("Compounds to screen:")
for n, s in zip(names, smiles_list):
    print(f"  {n:18s}  {s[:70]}")

print(f"\nDispatching KinaseDocker2 against all 8 kinase groups ...")

result = dispatch(
    "kinasedocker2",
    smiles          = smiles_list,
    kinase_families = ["AGC","CAMK","CK1","CMGC","Other","STE","TK","TKL"],
    docking_engine  = "vina",
    scoring_function= "DNN",
    run_name        = "PDK1_ligands_kinome_screen",
)

print("rc =", result.get("rc"))
print("summary:", result.get("summary","")[:500])
print("n_predictions:", result.get("n_predictions"))
print("results_csv:", result.get("results_csv"))
