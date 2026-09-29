
import numpy as np
import pathlib

session_dir = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb")
work_dir = session_dir / "brd4_vhl_protac"
pdb3 = work_dir / "3MXF.pdb"
pdb5 = work_dir / "5T35.pdb"

def apply_transform(coords_arr, R, t):
    return coords_arr @ R.T + t

def read_hetatm_ligand(path, chain_id, resname_filter=None):
    atoms = []
    with open(path) as f:
        for line in f:
            if line[:6].strip() == "HETATM" and line[21] == chain_id:
                rn = line[17:20].strip()
                if resname_filter and rn != resname_filter: continue
                name = line[12:16].strip()
                resnum = int(line[22:26])
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                atoms.append((name, resnum, rn, np.array([x, y, z])))
    return atoms

def read_ca_chain(path, chain_id):
    c = []; seen = set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn = int(line[22:26])
                if rn not in seen:
                    seen.add(rn)
                    x,y,z = float(line[30:38]),float(line[38:46]),float(line[46:54])
                    c.append(np.array([x,y,z]))
    return np.array(c)

def min_dist_to_chain(atom_coords, chain_ca):
    diffs = chain_ca - atom_coords
    return float(np.min(np.linalg.norm(diffs, axis=1)))

# Rf and tf are already in namespace from previous call
# JQ1 exit atom (farthest from BD1 CA centroid)
bd1_ca_arr = read_ca_chain(pdb3, 'A')
bd1_ca_cen = bd1_ca_arr.mean(axis=0)
jq1_atoms = read_hetatm_ligand(pdb3, 'A', 'JQ1')
jq1_to_bd1 = np.array([np.linalg.norm(a[3]-bd1_ca_cen) for a in jq1_atoms])
jq1_exit_idx = np.argmax(jq1_to_bd1)
jq1_exit_atom = jq1_atoms[jq1_exit_idx]
print(f"JQ1 exit atom: {jq1_exit_atom[0]}  dist_to_BD1_cen={jq1_to_bd1[jq1_exit_idx]:.2f} Å")

# Transform JQ1 exit to ternary frame
jq1_exit_tf = apply_transform(jq1_exit_atom[3].reshape(1,3), Rf, tf)[0]

# VHL-side exit: VHL-side MZ1 atom with max dist to VHL
mz1_atoms = read_hetatm_ligand(pdb5, 'D', '759')
bd2_ca_arr = read_ca_chain(pdb5, 'A')
vhl_ca_arr = read_ca_chain(pdb5, 'D')

mz1_bd_dists  = np.array([min_dist_to_chain(a[3], bd2_ca_arr) for a in mz1_atoms])
mz1_vhl_dists = np.array([min_dist_to_chain(a[3], vhl_ca_arr) for a in mz1_atoms])

bd_side_mask = mz1_bd_dists < mz1_vhl_dists
bd_exit_idx  = np.argmax(np.where(bd_side_mask,  mz1_bd_dists,  -99))
vhl_exit_idx = np.argmax(np.where(~bd_side_mask, mz1_vhl_dists, -99))

bd_exit_atom  = mz1_atoms[bd_exit_idx]
vhl_exit_atom = mz1_atoms[vhl_exit_idx]
bd_exit_xyz   = bd_exit_atom[3]
vhl_exit_xyz  = vhl_exit_atom[3]

mz1_bridge = np.linalg.norm(bd_exit_xyz - vhl_exit_xyz)
bd1_exit_to_vhl_exit = np.linalg.norm(jq1_exit_tf - vhl_exit_xyz)

print(f"MZ1 bridge (BD2 exit → VHL exit): {mz1_bridge:.4f} Å  (reported: 5.0)")
print(f"BD1 JQ1-exit → VHL exit (model):  {bd1_exit_to_vhl_exit:.4f} Å  (reported: 5.6)")

b = 1.5
n_star = (bd1_exit_to_vhl_exit / b)**2
print(f"\nn* = ({bd1_exit_to_vhl_exit:.4f}/{b})^2 = {n_star:.4f}")
print(f"n* printed to 1 dp = {n_star:.1f}  (reported: 13.8)")
print(f"d printed to 1 dp = {bd1_exit_to_vhl_exit:.1f}  (reported: 5.6)")
