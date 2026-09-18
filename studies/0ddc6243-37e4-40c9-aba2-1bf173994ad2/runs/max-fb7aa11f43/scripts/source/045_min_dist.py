
import os, numpy as np
from rdkit import Chem

pose_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/poses"
ref_pdb  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/85C_crystal.pdb"

def min_dist(lig_xyz, ref_pts):
    return float(np.min(np.linalg.norm(lig_xyz[:,None]-ref_pts[None,:], axis=2)))

# Reference 85C
ref_mol  = Chem.MolFromPDBFile(ref_pdb, sanitize=False, removeHs=True)
ref_xyz  = ref_mol.GetConformer().GetPositions()
print(f"85C crystal: CRBN_d={min_dist(ref_xyz,crbn_pts):.2f}  GSPT1_d={min_dist(ref_xyz,gspt1_pts):.2f}  ← reference\n")

CRBN_CUT, GSPT1_CUT = 4.0, 4.5

sdf_files = sorted([f for f in os.listdir(pose_dir) if f.endswith('_poses.sdf')])
print(f"{'Compound':<14} {'CNN_pose':>8} {'CNN_aff':>8} {'emp_aff':>8} {'CRBN_d':>7} {'GSPT1_d':>8}  Class")
print("-"*78)

rows = []
for sdf_fname in sdf_files:
    sdf_path = os.path.join(pose_dir, sdf_fname)
    sup  = Chem.SDMolSupplier(sdf_path, sanitize=False, removeHs=True)
    mols = [m for m in sup if m is not None]
    if not mols:
        print(f"{sdf_fname}: no valid molecules")
        continue

    # Top CNN-scored pose is mol[0] (GNINA ranks by CNN score)
    top = mols[0]
    props = {p: top.GetPropsAsDict().get(p) for p in
             ['minimizedAffinity','CNNscore','CNNaffinity',
              'affinity','cnn_pose_score','cnn_affinity']}

    xyz     = top.GetConformer().GetPositions()
    d_crbn  = min_dist(xyz, crbn_pts)
    d_gspt1 = min_dist(xyz, gspt1_pts)

    # Extract scores — try multiple property name variants GNINA uses
    emp   = props.get('minimizedAffinity') or props.get('affinity')
    cnn_p = props.get('CNNscore') or props.get('cnn_pose_score')
    cnn_a = props.get('CNNaffinity') or props.get('cnn_affinity')

    if emp is None:
        # read raw text
        with open(sdf_path) as f:
            raw = f.read()
        import re
        m = re.search(r'>.*?minimizedAffinity.*?<\n([^\n]+)', raw, re.DOTALL)
        emp = float(m.group(1)) if m else None

    if d_crbn<=CRBN_CUT and d_gspt1<=GSPT1_CUT: cls = "POTENTIAL GLUE"
    elif d_crbn<=CRBN_CUT:  cls = "CRBN-only"
    elif d_gspt1<=GSPT1_CUT: cls = "GSPT1-only"
    else: cls = "out-of-pocket"

    name = sdf_fname.replace('lig_0','').replace('_poses.sdf','').replace('_',' ')
    print(f"{name:<14} {str(cnn_p)[:8]:>8} {str(cnn_a)[:8]:>8} {str(emp)[:8]:>8} "
          f"{d_crbn:>7.2f} {d_gspt1:>8.2f}  {cls}")
    rows.append({'name':name,'cnn_pose':cnn_p,'cnn_aff':cnn_a,'emp_aff':emp,
                 'd_crbn':d_crbn,'d_gspt1':d_gspt1,'class':cls,'xyz':xyz,'n_poses':len(mols)})
