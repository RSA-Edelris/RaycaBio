
import gzip
from rdkit.Chem import SDWriter

# ── Print pose table without strict formatting ────────────────────────────────
print(f"Best Vina affinity: {O.get('best_affinity_kcal_mol')} kcal/mol")
print(f"Best CNN affinity:  {O.get('best_cnn_affinity')}")
print(f"Best CNN pose score:{O.get('best_cnn_pose_score')}")
print(f"GPU used: {O.get('gpu_used')}, num_poses: {O.get('num_poses')}\n")

for p in O.get("poses", []):
    print(f"  mode={p.get('mode')}  affinity={p.get('affinity_kcal_mol')} kcal/mol  "
          f"cnn_pose={p.get('cnn_pose_score')}  cnn_aff={p.get('cnn_affinity')}")

# ── Parse docked SDF.gz ───────────────────────────────────────────────────────
with gzip.open(f"{WS}/gnina_docked.sdf.gz", "rt") as fh:
    sdf_text = fh.read()

suppl = SDMolSupplier()
suppl.SetData(sdf_text, removeHs=False, sanitize=True)
pose_mols = [m for m in suppl if m is not None]
print(f"\nParsed {len(pose_mols)} poses from SDF")
print("Pose 1 props:", list(pose_mols[0].GetPropsAsDict().keys()) if pose_mols else "none")

# Save individual pose SDFs
pose_paths = []
for i, mol in enumerate(pose_mols[:5]):
    mol.SetProp("_Name", f"EL2003A-A2U1_pose{i+1}")
    path = f"{WS}/pose_{i+1}.sdf"
    w = SDWriter(path)
    w.write(mol)
    w.close()
    pose_paths.append(path)
    print(f"  pose_{i+1}.sdf: {list(mol.GetPropsAsDict().keys())}")

# Save all 5 poses in a single combined SDF for the report
all_path = f"{WS}/EL2003A-A2U1_all5poses.sdf"
w = SDWriter(all_path)
for mol in pose_mols[:5]:
    w.write(mol)
w.close()
print(f"\nAll-poses SDF: {all_path}")
