
import subprocess, os

# Step 1: Determine ligand net charge from protonated SMILES
# [NH+] → net charge = +1
from rdkit.Chem import rdmolops
suppl_lig2 = Chem.SDMolSupplier('ligand_prepared.sdf', removeHs=True)
mol_charged = [m for m in suppl_lig2 if m is not None][0]
net_charge = rdmolops.GetFormalCharge(mol_charged)
print(f"Ligand net formal charge: {net_charge}")

# Step 2: antechamber — GAFF2 parameterization
# Input: best pose mol (SDF with explicit H → use ligand_prepared.sdf)
r_ac = subprocess.run([
    'antechamber',
    '-i', 'ligand_prepared.sdf', '-fi', 'sdf',
    '-o', 'ligand.mol2',         '-fo', 'mol2',
    '-c', 'bcc',                  # AM1-BCC charges
    '-nc', str(net_charge),
    '-at', 'gaff2',
    '-rn', 'LIG',
    '-dr', 'n'                    # no ring detection warnings
], capture_output=True, text=True, cwd=WS)

print("antechamber rc:", r_ac.returncode)
if r_ac.returncode != 0:
    print("STDOUT:", r_ac.stdout[-1000:])
    print("STDERR:", r_ac.stderr[-500:])
else:
    sz = os.path.getsize(f'{WS}/ligand.mol2')
    print(f"ligand.mol2: {sz} bytes")
