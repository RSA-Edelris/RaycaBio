
from rdkit import Chem
import numpy as np

# Identify best pose per ligand (lowest MM-GBSA)
best_poses = {}
for lig in ligand_names:
    lig_rows = [r for r in full_table if r['mol_name'] == lig]
    best = min(lig_rows, key=lambda r: r['mmgbsa'])
    best_poses[lig] = best
    print(f"{lig:22s}  best_rank={best['rank']}  ΔG={best['mmgbsa']:.3f}  aff={best['affinity']:.3f}")

print("\nBest pose files:")
for lig, row in best_poses.items():
    fname = f"{ART}/all_poses/{lig}_pose{row['rank']}.sdf"
    exists = os.path.exists(fname)
    print(f"  {fname}  exists={exists}")
