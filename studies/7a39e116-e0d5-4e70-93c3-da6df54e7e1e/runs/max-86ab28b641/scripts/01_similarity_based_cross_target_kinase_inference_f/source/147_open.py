
import json
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
with open(f"{WS}/ligand_smiles.json") as f:
    lig_data = json.load(f)
for name, v in lig_data.items():
    print(f"{name}: {v['smiles']}")
