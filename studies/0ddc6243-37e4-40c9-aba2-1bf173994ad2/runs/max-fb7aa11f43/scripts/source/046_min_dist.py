
import os, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

pose_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/poses"
lig_dir  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/ligands"

def min_dist(lig_xyz, ref_pts):
    return float(np.min(np.linalg.norm(lig_xyz[:,None]-ref_pts[None,:], axis=2)))

# Glutarimide SMARTS: the N-H flanked by two carbonyls in a 6-membered ring
# Pattern: N with two adjacent C=O, ring size 6
GLUTARIMIDE_SMARTS = Chem.MolFromSmarts('[NH1]1CCC(=O)NC1=O')   # glutarimide ring
GLUT_SMARTS2       = Chem.MolFromSmarts('C(=O)[NH1]C(=O)')       # simpler: N-H between two C=O

sdf_files = sorted([f for f in os.listdir(pose_dir) if f.endswith('_poses.sdf')])
lig_files  = sorted([f for f in os.listdir(lig_dir)  if f.endswith('.sdf')])

print(f"{'Compound':<14} {'CRBN_d(all)':>11} {'CRBN_d(glut)':>13} {'GSPT1_d(all)':>13}  Glut_anchored?")
print("-"*75)

for sdf_fname, lig_fname in zip(sdf_files, lig_files):
    # Top pose
    sup = Chem.SDMolSupplier(os.path.join(pose_dir, sdf_fname), sanitize=True, removeHs=False)
    top = next(iter(sup), None)
    if top is None: continue

    xyz_all = top.GetConformer().GetPositions()

    # Find glutarimide atoms
    glut_match = top.GetSubstructMatches(GLUTARIMIDE_SMARTS)
    if not glut_match:
        glut_match = top.GetSubstructMatches(GLUT_SMARTS2)
    if not glut_match:
        # try without explicit H (after sanitise)
        glut_match = top.GetSubstructMatches(Chem.MolFromSmarts('[NX3;H1]1CCC(=O)[NX3;H1]C1=O'))

    if glut_match:
        glut_idx = list(glut_match[0])
        xyz_glut = xyz_all[glut_idx]
        d_crbn_glut = min_dist(xyz_glut, crbn_pts)
    else:
        glut_idx, xyz_glut, d_crbn_glut = [], None, 999.0

    d_crbn_all  = min_dist(xyz_all, crbn_pts)
    d_gspt1_all = min_dist(xyz_all, gspt1_pts)

    anchored = "YES" if d_crbn_glut <= 4.0 else ("NO_MATCH" if not glut_match else "NO")

    name = sdf_fname.replace('lig_0','').replace('_poses.sdf','').replace('_',' ')
    print(f"{name:<14} {d_crbn_all:>11.2f} {d_crbn_glut:>13.2f} {d_gspt1_all:>13.2f}  {anchored}  "
          f"({len(glut_idx)} glut atoms)")
