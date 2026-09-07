
ART = "/home/ubuntu/rayca-artifacts/cacaa3ede77705c5b065320a/files"

result_dock = dispatch("gnina", {
    "proteinFile": f"{ART}/1Z5M_receptor_pH7.4.pdb",
    "ligandFile":  f"{ART}/ligand_clean_PDK1.sdf",
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

print("rc:", result_dock.get("rc"))
print("summary:", result_dock.get("summary",""))
print("gpu_used:", result_dock.get("gpu_used"))
print("num_poses:", result_dock.get("num_poses"))
print("best_affinity:", result_dock.get("best_affinity_kcal_mol"))
poses = result_dock.get("poses",[])
for p in poses:
    print(f"  mode {p.get('mode')}: {p.get('affinity_kcal_mol')} kcal/mol  cnn_pose={p.get('cnn_pose_score','?')}  cnn_aff={p.get('cnn_affinity','?')}")
