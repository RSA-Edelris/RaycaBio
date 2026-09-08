
from rdkit.Chem import SDWriter
import os

poses_dir = f"{ART}/all_poses"
os.makedirs(poses_dir, exist_ok=True)

# Save all 5 poses per ligand into per-ligand SDF files
ligand_names = list(dict.fromkeys(r['mol_name'] for r in pose_table))  # preserve order

for lig_name in ligand_names:
    lig_poses = [r for r in pose_table if r['mol_name'] == lig_name]
    out_sdf = f"{poses_dir}/{lig_name}_5poses.sdf"
    with open(out_sdf, 'w') as fh:
        for r in lig_poses:
            fh.write(r['block'] + '\n$$$$\n')
    print(f"  {lig_name}: {len(lig_poses)} poses → {os.path.basename(out_sdf)}")

# Save best pose per ligand (by CNNscore) as individual SDF files
print("\nBest pose per ligand (by CNNscore):")
best_poses = {}
for lig_name in ligand_names:
    lig_poses = [r for r in pose_table if r['mol_name'] == lig_name]
    best = max(lig_poses, key=lambda r: r['cnn_score'])
    best_poses[lig_name] = best
    out_sdf = f"{poses_dir}/{lig_name}_best.sdf"
    with open(out_sdf, 'w') as fh:
        fh.write(best['block'] + '\n$$$$\n')
    print(f"  {lig_name:22s}  rank={best['rank']}  aff={best['affinity']:.4f}  "
          f"CNN={best['cnn_score']:.4f}  CNNaff={best['cnn_aff']:.4f}")

print(f"\nAll poses saved to {poses_dir}/")
