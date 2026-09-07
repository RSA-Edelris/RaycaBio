
from rdkit import Chem
from rdkit.Chem import AllChem
import subprocess, os

# Add explicit hydrogens and write proper 3D SDF for antechamber
mol = Chem.MolFromMolFile(best_sdf, removeHs=False)
mol_h = AllChem.AddHs(mol, addCoords=True)

# Confirm geometry is reasonable (should already have 3D from docking)
conf = mol_h.GetConformer()
print(f"Atoms with H: {mol_h.GetNumAtoms()}")

lig_h_sdf = f'{MD_DIR}/ligand_h.sdf'
with Chem.SDWriter(lig_h_sdf) as w:
    w.write(mol_h)
print(f"Written: {lig_h_sdf}")

# Run antechamber: SDF → GAFF2 mol2 with AM1-BCC charges, residue name LIG
lig_mol2 = f'{MD_DIR}/ligand.mol2'
cmd = [
    'antechamber',
    '-i', lig_h_sdf, '-fi', 'sdf',
    '-o', lig_mol2, '-fo', 'mol2',
    '-c', 'bcc',          # AM1-BCC charges
    '-nc', str(net_charge),
    '-rn', 'LIG',
    '-at', 'gaff2',
    '-s', '2',            # verbose
    '-pf', 'y',           # remove tmp files
]
print("Running antechamber (AM1-BCC charges, ~2-3 min)...")
r = subprocess.run(cmd, capture_output=True, text=True, cwd=MD_DIR)
print(r.stdout[-1000:] if len(r.stdout) > 1000 else r.stdout)
if r.returncode != 0:
    print("STDERR:", r.stderr[-500:])
else:
    print(f"mol2 written: {os.path.exists(lig_mol2)}, size: {os.path.getsize(lig_mol2)}")
