
import os, subprocess
from rdkit import Chem
from rdkit.Chem import AllChem

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
MD_DIR = f'{WD}/md_EDS01806218_ent2'
os.makedirs(MD_DIR, exist_ok=True)

# ── Extract best pose (pose 0) from SDF ──────────────────────────────────
sdf_path = f'{WD}/poses_EDS01806218_ent2.sdf'
with open(sdf_path) as fh:
    content = fh.read()

# Split on $$$$ separator
blocks = [b.strip() for b in content.split('$$$$') if b.strip()]
print(f"Total poses in SDF: {len(blocks)}")

# Write best pose (index 0) as SDF
best_sdf = f'{MD_DIR}/ligand_best.sdf'
with open(best_sdf, 'w') as fh:
    fh.write(blocks[0] + '\n$$$$\n')

# Load with RDKit to confirm
mol = Chem.MolFromMolBlock(blocks[0], removeHs=False)
if mol is None:
    mol = Chem.MolFromMolBlock(blocks[0], removeHs=True, sanitize=False)
    Chem.SanitizeMol(mol)
print(f"Ligand atoms: {mol.GetNumAtoms()} (with H: {mol.GetNumAtoms()})")
print(f"Heavy atoms: {sum(1 for a in mol.GetAtoms() if a.GetAtomicNum() > 1)}")
print(f"Formula: {Chem.rdMolDescriptors.CalcMolFormula(mol)}")

# Get net formal charge
net_charge = sum(a.GetFormalCharge() for a in mol.GetAtoms())
print(f"Net formal charge: {net_charge}")
print(f"Best pose SDF written to: {best_sdf}")
