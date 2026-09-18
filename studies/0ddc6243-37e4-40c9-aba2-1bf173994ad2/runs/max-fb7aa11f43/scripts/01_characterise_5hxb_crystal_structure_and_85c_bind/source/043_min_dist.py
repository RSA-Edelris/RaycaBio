
import os, numpy as np
from rdkit import Chem

pose_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/poses"

def min_dist(lig_xyz, ref_pts):
    """Minimum distance between any ligand atom and any ref point."""
    if len(ref_pts) == 0: return 999.0
    d = np.min(np.linalg.norm(lig_xyz[:, None] - ref_pts[None, :], axis=2))
    return float(d)

# Also load crystal 85C for reference
ref_pdb  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/85C_crystal.pdb"
ref_mol  = Chem.MolFromPDBFile(ref_pdb, sanitize=False, removeHs=True)
if ref_mol:
    ref_xyz = ref_mol.GetConformer().GetPositions()
    d_crbn  = min_dist(ref_xyz, crbn_pts)
    d_gspt1 = min_dist(ref_xyz, gspt1_pts)
    print(f"85C crystal  CRBN_d={d_crbn:.2f}  GSPT1_d={d_gspt1:.2f}  ← reference")
else:
    print("WARNING: could not load 85C crystal")

print("\n{:<16} {:>8} {:>8} {:>8} {:>9} {:>10}  {}".format(
    "Compound", "CNN_pose", "CNN_aff", "emp_aff", "CRBN_d", "GSPT1_d", "Class"))
print("-"*80)

glue_threshold_crbn  = 4.0   # Å
glue_threshold_gspt1 = 4.5   # Å

for row in summary_rows:
    sdf_path = os.path.join(pose_dir, row['fname'].replace('.sdf','_poses.sdf'))
    supplier = Chem.SDMolSupplier(sdf_path, sanitize=False, removeHs=True)
    top_mol  = next(iter(supplier), None)

    if top_mol is None:
        print(f"{row['name']:<16}  NO POSE")
        continue

    xyz    = top_mol.GetConformer().GetPositions()
    d_crbn  = min_dist(xyz, crbn_pts)
    d_gspt1 = min_dist(xyz, gspt1_pts)

    # Classification
    crbn_contact  = d_crbn  <= glue_threshold_crbn
    gspt1_contact = d_gspt1 <= glue_threshold_gspt1
    if crbn_contact and gspt1_contact:
        cls = "POTENTIAL GLUE"
    elif crbn_contact:
        cls = "CRBN only"
    elif gspt1_contact:
        cls = "GSPT1 only"
    else:
        cls = "out-of-pocket"

    # Store back
    row['d_crbn']  = d_crbn
    row['d_gspt1'] = d_gspt1
    row['class']   = cls

    print(f"{row['name']:<16} {row['top_cnn_pose']:>8.3f} {row['top_cnn_aff']:>8.2f} "
          f"{row['top_emp_aff']:>8.2f} {d_crbn:>9.2f} {d_gspt1:>10.2f}  {cls}")
