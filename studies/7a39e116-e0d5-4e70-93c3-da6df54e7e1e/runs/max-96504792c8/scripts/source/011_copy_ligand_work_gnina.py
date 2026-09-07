
import shutil

# Copy ligand to /work for gnina
lig_src = f"{WS}/ligand_clean_PDK1.sdf"
shutil.copy(lig_src, f"{WORK}/ligand_clean_PDK1.sdf")
print("Ligand copied to /work")

# Verify both files present
import os
print("Receptor in /work:", os.path.exists(f"{WORK}/1Z5M_receptor_pH7.4.pdb"))
print("Ligand in /work:", os.path.exists(f"{WORK}/ligand_clean_PDK1.sdf"))
print(f"Box center: ({cx:.2f}, {cy:.2f}, {cz:.2f})")
print(f"Box size: {box_size} x {box_size} x {box_size} Å")

# Run gnina - 5 poses, CNN rescore, exhaustiveness 16 for a tight defined pocket
result_dock = dispatch("gnina", {
    "proteinFile": "1Z5M_receptor_pH7.4.pdb",
    "ligandFile": "ligand_clean_PDK1.sdf",
    "boxX": float(cx),
    "boxY": float(cy),
    "boxZ": float(cz),
    "width":  float(box_size),
    "height": float(box_size),
    "depth":  float(box_size),
    "numModes": 5,
    "exhaustiveness": 16,
    "cnnScoring": "rescore",
    "seed": 42
}, gpu=True)

print("\ngnina rc:", result_dock.get("rc"))
print("gpu_used:", result_dock.get("gpu_used"))
print("num_poses:", result_dock.get("num_poses"))
print("best_affinity:", result_dock.get("best_affinity_kcal_mol"), "kcal/mol")
print("best_cnn_affinity:", result_dock.get("best_cnn_affinity"))
print("best_cnn_pose_score:", result_dock.get("best_cnn_pose_score"))
print("output_file:", result_dock.get("output_file",""))
print("summary:", result_dock.get("summary",""))

poses = result_dock.get("poses", [])
print(f"\nAll {len(poses)} poses:")
for p in poses:
    print(f"  mode {p.get('mode')}: affinity={p.get('affinity_kcal_mol')} "
          f"cnn_pose={p.get('cnn_pose_score','?'):.3f} "
          f"cnn_aff={p.get('cnn_affinity','?')}")
