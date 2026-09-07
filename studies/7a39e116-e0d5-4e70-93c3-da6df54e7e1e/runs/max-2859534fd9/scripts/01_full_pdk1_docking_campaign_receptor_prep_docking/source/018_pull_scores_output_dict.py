
import gzip
from rdkit.Chem import SDMolSupplier, SDWriter
from io import BytesIO, StringIO

# ── Pull scores from the output dict ─────────────────────────────────────────
O = result_dock["output"]
print("best_affinity_kcal_mol:", O.get("best_affinity_kcal_mol"))
print("best_cnn_affinity:", O.get("best_cnn_affinity"))
print("best_cnn_pose_score:", O.get("best_cnn_pose_score"))
print("num_poses:", O.get("num_poses"))
print("gpu_used:", O.get("gpu_used"))
print()
poses_meta = O.get("poses", [])
print(f"Pose table ({len(poses_meta)} entries):")
for p in poses_meta:
    print(f"  mode {p.get('mode'):>2}: affinity={p.get('affinity_kcal_mol'):>7}  "
          f"cnn_pose={p.get('cnn_pose_score',0):.3f}  "
          f"cnn_aff={p.get('cnn_affinity',0):.3f}")

# ── Parse docked SDF.gz → individual pose PDB files for MD ───────────────────
gz_path = f"{WS}/gnina_docked.sdf.gz"
with gzip.open(gz_path, "rt") as fh:
    sdf_text = fh.read()

suppl = SDMolSupplier()
suppl.SetData(sdf_text, removeHs=False, sanitize=True)
pose_mols = [m for m in suppl if m is not None]
print(f"\nParsed {len(pose_mols)} pose molecules from SDF")

# Save individual pose SDF files for MD setup
from rdkit.Chem import MolToMolBlock
pose_paths = []
for i, mol in enumerate(pose_mols[:5]):
    mol.SetProp("_Name", f"EL2003A-A2U1_pose{i+1}")
    path = f"{WS}/pose_{i+1}.sdf"
    w = SDWriter(path)
    w.write(mol)
    w.close()
    pose_paths.append(path)
    
print(f"Saved {len(pose_paths)} pose SDF files to workspace")

# Cross-check: print all props of pose 1
print("\nPose 1 properties:", dict(pose_mols[0].GetPropsAsDict()))
