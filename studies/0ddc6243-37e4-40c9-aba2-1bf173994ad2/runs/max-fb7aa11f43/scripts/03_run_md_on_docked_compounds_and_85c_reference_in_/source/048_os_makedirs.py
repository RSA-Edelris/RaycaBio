
import os
from rdkit import Chem
from rdkit.Chem import AllChem

pose_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/poses"
top_dir  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/md/ligands"
os.makedirs(top_dir, exist_ok=True)

# Map compound names to short IDs for AMBER (no spaces)
compound_map = {
    'lig_00_Compound_1_poses.sdf':  ('CPD1',  0),
    'lig_01_Compound_4_poses.sdf':  ('CPD4',  0),
    'lig_02_Compound_7_poses.sdf':  ('CPD7',  0),
    'lig_03_Compound_8_poses.sdf':  ('CPD8',  0),
    'lig_04_Compound_9_poses.sdf':  ('CPD9',  0),
    'lig_05_Compound_10_poses.sdf': ('CPD10', 0),
    'lig_06_Compound_11_poses.sdf': ('CPD11', 0),
    'lig_07_Compound_12_poses.sdf': ('CPD12', 0),
}

# Net charges for each compound (inspect SMILES for charge)
# All neutral forms as supplied
net_charges = {
    'CPD1': 0, 'CPD4': 0, 'CPD7': 0, 'CPD8': 0,
    'CPD9': 0, 'CPD10': 0, 'CPD11': 0, 'CPD12': 0,
}

# Extract top pose (mol[0]) as single-molecule SDF
for fname, (cid, _) in compound_map.items():
    src = os.path.join(pose_dir, fname)
    sup = Chem.SDMolSupplier(src, sanitize=True, removeHs=False)
    top = next(iter(sup), None)
    if top is None:
        print(f"ERROR: no mol in {fname}")
        continue
    out_sdf = os.path.join(top_dir, f"{cid}_top.sdf")
    w = Chem.SDWriter(out_sdf)
    w.write(top)
    w.close()
    n_atoms = top.GetNumAtoms()
    print(f"{cid}: {n_atoms} atoms → {os.path.basename(out_sdf)}")

# Also stage the 85C crystal ligand as SDF
ref_pdb = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/85C_crystal.pdb"
ref_mol = Chem.MolFromPDBFile(ref_pdb, sanitize=True, removeHs=False)
if ref_mol:
    ref_out = os.path.join(top_dir, "REF_85C_top.sdf")
    w = Chem.SDWriter(ref_out)
    w.write(ref_mol)
    w.close()
    print(f"REF_85C: {ref_mol.GetNumAtoms()} atoms → REF_85C_top.sdf")
