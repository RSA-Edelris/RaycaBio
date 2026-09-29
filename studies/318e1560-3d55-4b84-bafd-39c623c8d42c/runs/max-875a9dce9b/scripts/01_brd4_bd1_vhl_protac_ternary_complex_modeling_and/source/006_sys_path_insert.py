
import sys
sys.path.insert(0, str(work_dir))
from helpers import read_ca_coords, read_hetatm_ligand, kabsch, apply_transform, rmsd, read_all_atom_coords

pdb3 = work_dir / "3MXF.pdb"
pdb5 = work_dir / "5T35.pdb"

# Reload CA coords
bd1_ca = read_ca_coords(pdb3, 'A')
bd2_ca = read_ca_coords(pdb5, 'A')
bd1_res = sorted(bd1_ca.keys())
bd2_res = sorted(bd2_ca.keys())

# Align first 111 residues of BD1 → BD2 (sequential, same fold)
n_align = 111
mobile_arr  = np.array([bd1_ca[r] for r in bd1_res[:n_align]])
target_arr  = np.array([bd2_ca[r] for r in bd2_res[:n_align]])

R, t = kabsch(mobile_arr, target_arr)
mobile_fit  = apply_transform(mobile_arr, R, t)
print(f"BD1→BD2 Cα RMSD over {n_align} residues: {rmsd(mobile_fit, target_arr):.2f} Å")

# Read JQ1 from 3MXF (chain A, resname JQ1)
jq1_atoms = read_hetatm_ligand(pdb3, 'A', 'JQ1')
print(f"\nJQ1 atoms in 3MXF: {len(jq1_atoms)}")
for a in jq1_atoms[:5]:
    print(f"  {a[0]:4s}  {a[3]}")

# Read MZ1 (759) from 5T35 chain D (VHL chain)
mz1_atoms = read_hetatm_ligand(pdb5, 'D', '759')
print(f"\nMZ1 (759) atoms in 5T35 chain D: {len(mz1_atoms)}")
for a in mz1_atoms[:5]:
    print(f"  {a[0]:4s}  {a[3]}")
