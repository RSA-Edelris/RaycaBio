
import time, json

ART = ws   # workspace = artifact dir for this session

print("Dispatching gnina — 6 ligands, 5 poses each, GPU, exhaustiveness=16 ...")
t0 = time.time()

result_dock = dispatch("gnina", {
    "proteinFile": "1Z5M_receptor_pH7.4.pdb",
    "ligandFile":  "ligand_clean_PDK1.sdf",
    "boxX":   float(cx),
    "boxY":   float(cy),
    "boxZ":   float(cz),
    "width":  float(box_size),
    "height": float(box_size),
    "depth":  float(box_size),
    "numModes": 5,
    "exhaustiveness": 16,
    "cnnScoring": "rescore",
    "seed": 42
}, files={
    "1Z5M_receptor_pH7.4.pdb": f"{ART}/1Z5M_receptor_pH7.4.pdb",
    "ligand_clean_PDK1.sdf":   f"{ART}/ligand_clean_PDK1.sdf"
}, gpu=True)

elapsed = time.time() - t0
print(f"Done in {elapsed:.1f}s")
print(f"rc={result_dock.get('rc')}  gpu={result_dock.get('gpu_used')}  "
      f"num_poses={result_dock.get('num_poses')}  "
      f"best_affinity={result_dock.get('best_affinity_kcal_mol')} kcal/mol")
print(f"best_cnn_affinity={result_dock.get('best_cnn_affinity')}  "
      f"best_cnn_pose={result_dock.get('best_cnn_pose_score')}")

poses = result_dock.get("poses", [])
print(f"\nAll {len(poses)} poses across all ligands:")
for p in poses:
    print(f"  lig={p.get('ligand_name','?'):20s}  mode={p.get('mode')}  "
          f"aff={p.get('affinity_kcal_mol'):7.3f}  "
          f"cnn_pose={p.get('cnn_pose_score','?')}  cnn_aff={p.get('cnn_affinity','?')}")

# Save raw result
with open(f"{ART}/gnina_all6_result.json", "w") as fh:
    json.dump(result_dock, fh, indent=2)
print(f"\nRaw result saved.")
