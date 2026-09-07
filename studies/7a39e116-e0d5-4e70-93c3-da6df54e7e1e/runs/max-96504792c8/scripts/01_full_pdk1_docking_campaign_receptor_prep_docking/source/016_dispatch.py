
result_dock = dispatch("gnina", {
    "proteinFile": "1Z5M_receptor_pH7.4.pdb",
    "ligandFile":  "ligand_clean_PDK1.sdf",
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
}, files={
    "1Z5M_receptor_pH7.4.pdb": f"{ART}/1Z5M_receptor_pH7.4.pdb",
    "ligand_clean_PDK1.sdf":  f"{ART}/ligand_clean_PDK1.sdf"
}, gpu=True)

print("rc:", result_dock.get("rc"))
print("summary:", result_dock.get("summary",""))
print("gpu_used:", result_dock.get("gpu_used"))
print("num_poses:", result_dock.get("num_poses"))
print("best_affinity:", result_dock.get("best_affinity_kcal_mol"), "kcal/mol")
print("best_cnn_affinity:", result_dock.get("best_cnn_affinity"))
print("best_cnn_pose_score:", result_dock.get("best_cnn_pose_score"))
print("output_file:", result_dock.get("output_file",""))

poses = result_dock.get("poses", [])
print(f"\nAll {len(poses)} poses:")
for p in poses:
    print(f"  mode {p.get('mode')}: affinity={p.get('affinity_kcal_mol')} kcal/mol  "
          f"cnn_pose={p.get('cnn_pose_score','?')}  cnn_aff={p.get('cnn_affinity','?')}")
