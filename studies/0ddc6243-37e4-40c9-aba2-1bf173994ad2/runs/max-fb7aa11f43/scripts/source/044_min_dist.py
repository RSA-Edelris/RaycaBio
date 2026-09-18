
import os, numpy as np
from rdkit import Chem

pose_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/poses"

def min_dist(lig_xyz, ref_pts):
    d = np.min(np.linalg.norm(lig_xyz[:, None] - ref_pts[None, :], axis=2))
    return float(d)

# Rebuild summary_rows from the persistent results dict
compounds = [
    "lig_00_Compound_1.sdf",
    "lig_01_Compound_4.sdf",
    "lig_02_Compound_7.sdf",
    "lig_03_Compound_8.sdf",
    "lig_04_Compound_9.sdf",
    "lig_05_Compound_10.sdf",
    "lig_06_Compound_11.sdf",
    "lig_07_Compound_12.sdf",
]
summary_rows = []
for fname in compounds:
    r  = results[fname]
    op = r['output']
    row = {
        'name':        fname.split('.')[0],
        'fname':       fname,
        'top_cnn_pose': op['best_cnn_pose_score'],
        'top_cnn_aff':  op['best_cnn_affinity'],
        'top_emp_aff':  op['poses'][0]['affinity'],
        'best_emp_aff': min(p['affinity'] for p in op['poses']),
        'poses':        op['poses'],
    }
    summary_rows.append(row)

# Reference: 85C crystal contacts
ref_pdb = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/85C_crystal.pdb"
ref_mol = Chem.MolFromPDBFile(ref_pdb, sanitize=False, removeHs=True)
ref_xyz = ref_mol.GetConformer().GetPositions()
print(f"85C crystal  CRBN_d={min_dist(ref_xyz,crbn_pts):.2f}  GSPT1_d={min_dist(ref_xyz,gspt1_pts):.2f}  ← reference\n")

print(f"{'Compound':<16} {'CNN_pose':>8} {'CNN_aff':>8} {'emp_aff':>8} {'CRBN_d':>8} {'GSPT1_d':>9}  Class")
print("-"*82)

CRBN_CUT  = 4.0
GSPT1_CUT = 4.5

for row in summary_rows:
    sdf_path = os.path.join(pose_dir, row['fname'].replace('.sdf','_poses.sdf'))
    sup  = Chem.SDMolSupplier(sdf_path, sanitize=False, removeHs=True)
    mol  = next(iter(sup), None)
    if mol is None:
        print(f"{row['name']:<16}  NO POSE")
        continue
    xyz      = mol.GetConformer().GetPositions()
    d_crbn   = min_dist(xyz, crbn_pts)
    d_gspt1  = min_dist(xyz, gspt1_pts)
    row.update({'d_crbn': d_crbn, 'd_gspt1': d_gspt1, 'xyz': xyz})

    if d_crbn <= CRBN_CUT and d_gspt1 <= GSPT1_CUT:
        cls = "POTENTIAL GLUE"
    elif d_crbn <= CRBN_CUT:
        cls = "CRBN-only"
    elif d_gspt1 <= GSPT1_CUT:
        cls = "GSPT1-only"
    else:
        cls = "out-of-pocket"
    row['class'] = cls

    label = row['name'].replace('lig_0','Cpd ').replace('_',' ')
    print(f"{label:<16} {row['top_cnn_pose']:>8.3f} {row['top_cnn_aff']:>8.2f} "
          f"{row['top_emp_aff']:>8.2f} {d_crbn:>8.2f} {d_gspt1:>9.2f}  {cls}")
