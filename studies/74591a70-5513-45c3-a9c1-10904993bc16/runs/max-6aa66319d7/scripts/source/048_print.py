
from modulon.governance.toolkit import run_aidd_tool
import json

WORK = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
RECEPTOR = f"{WORK}/4CI2_receptor_for_docking.pdb"

missing = [
    {"name": "EDEL-CRBN-0002",     "file": f"{WORK}/ligands/lig3.sdf"},
    {"name": "EDEL-CRBN-0003",     "file": f"{WORK}/ligands/lig5.sdf"},
    {"name": "EDEL-CRBN-0003_ent", "file": f"{WORK}/ligands/lig6.sdf"},
]

missing_results = {}
for lig in missing:
    print(f"Docking {lig['name']}...")
    try:
        result = run_aidd_tool(
            "gnina",
            {
                "proteinFile": RECEPTOR,
                "ligandFile":  lig["file"],
                "boxX": 84.800, "boxY": 154.937, "boxZ": 13.242,
                "width": 24, "height": 24, "depth": 24,
                "numModes": 5,
                "cnnScoring": "rescore",
                "seed": 0,
            }
        )
        missing_results[lig["name"]] = result
        print(f"  Done: affinity={result.get('best_affinity_kcal_mol')} cnn={result.get('best_cnn_affinity')} poses={result.get('num_poses')}")
    except Exception as e:
        missing_results[lig["name"]] = {"error": str(e)}
        print(f"  FAILED: {e}")

print("\nAll 3 missing ligands processed.")
